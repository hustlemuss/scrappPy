import requests
from bs4 import BeautifulSoup
import json


def parse_headhunter_vacancies(city='Москва, Санкт-Петербург', keyword='Python'):
    base_url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    params = {
        'text': keyword,
        'area': 1,  # 1 - Москва, 2 - Санкт-Петербург
        'fromSearchLine': True
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36'
    }

    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    vacancies = []
    for vacancy in soup.find_all('div', class_='vacancy-serp-item'):
        title_element = vacancy.find('a', class_='bloko-link')
        if title_element:
            title = title_element.text.strip()
            link = title_element['href']
            company_element = vacancy.find('a', class_='bloko-link bloko-link_secondary')
            if company_element:
                company = company_element.text.strip()
            else:
                company = 'Не указано'
            salary_element = vacancy.find('div', class_='vacancy-serp-item__sidebar')
            if salary_element:
                salary_text = salary_element.text.strip()
            else:
                salary_text = 'Не указано'

            # Проверяем наличие ключевых слов в описании
            description_link = link
            description_response = requests.get(description_link, headers=headers)
            description_soup = BeautifulSoup(description_response.text, 'html.parser')
            description_text = description_soup.find('div', class_='vacancy-description').text
            if 'Django' in description_text and 'Flask' in description_text:
                city = city.split(',')[0].strip()  # Получаем только название города
                vacancies.append({
                    'title': title,
                    'link': link,
                    'company': company,
                    'salary': salary_text,
                    'city': city
                })

    return vacancies


if __name__ == '__main__':
    vacancies = parse_headhunter_vacancies()
    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)
