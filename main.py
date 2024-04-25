import requests
from bs4 import BeautifulSoup
import json


def parse_headhunter_vacancies():
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/107 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    vacancies = []

    for vacancy in soup.find_all('a', class_='bloko-link', target='_blank'):
        title_element = vacancy.find('span', class_='serp-item__title')
        if title_element:
            title = title_element.text.strip()
            link = vacancy['href']
            company_element = vacancy.find_next('a', class_='bloko-link', target='_blank')
            if company_element:
                company = company_element.text.strip()
            else:
                company = 'Не указано'
            salary_element = vacancy.find_next('div', class_='vacancy-serp-item__sidebar')
            if salary_element:
                salary_text = salary_element.text.strip()
            else:
                salary_text = 'Не указано'

            # Проверяем наличие ключевых слов в описании и в заголовке
            description_response = requests.get(link, headers=headers)
            description_soup = BeautifulSoup(description_response.text, 'html.parser')
            description_text = ''
            description_element = description_soup.find('div', class_='g-user-content',
                                                        attrs={'data-qa': 'vacancy-description'})
            if description_element:
                description_text = description_element.text.strip()

            title_text = title.lower()

            # Проверяем наличие требований к вакансии в описании
            if 'django' in description_text.lower() and 'flask' in description_text.lower():
                city = 'Москва' if 'area=1' in url else 'Санкт-Петербург'
                vacancies.append({
                    'title': title,
                    'link': link,
                    'company': company,
                    'salary': salary_text,
                    'city': city,
                    'company_name': company,  # Добавляем название компании
                    'salary_range': salary_text  # Добавляем диапазон зарплаты
                })

    return vacancies


if __name__ == '__main__':
    vacancies = parse_headhunter_vacancies()
    if vacancies:
        with open('vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)