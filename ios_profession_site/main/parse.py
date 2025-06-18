import os
import requests
import time
import re
import django
import sys

from datetime import datetime, timedelta, timezone

# Добавляем в sys.path корень проекта (если ты внутри /app/main)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Указываем Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ios_profession_site.settings')

# Инициализируем Django
django.setup()

from main.models import HHStatistics


def get_vacancies(per_page=50):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "iOS разработчик",
        "specialization": 1,
        "per_page": per_page,
        "order_by": "publication_time",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    vacancies = response.json().get("items", [])
    vacancies_ios = [v for v in vacancies if "ios" in v.get("name").lower() and "разработчик" in v.get("name").lower()]
    vacancies_with_salary = [v for v in vacancies_ios if v.get("salary") is not None]
    return vacancies_with_salary

def get_vacancy_details(vacancy_id):
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def format_salary(salary):
    if not salary:
        return "Не указана"
    salary_from = salary.get("from")
    salary_to = salary.get("to")
    currency = salary.get("currency", "")
    if salary_from and salary_to:
        return f"{salary_from} - {salary_to} {currency}"
    elif salary_from:
        return f"от {salary_from} {currency}"
    elif salary_to:
        return f"до {salary_to} {currency}"
    return "Не указана"

def is_ios_developer(details):
    keywords = ["ios", "swift", "objective-c", "ios developer", "ios разработчик"]
    name = details.get("name", "").lower()
    description = details.get("description", "").lower()
    combined = name + " " + description
    return any(k in combined for k in keywords)


def time_until_older_than_24h(published_at_str):
    published_time = datetime.fromisoformat(published_at_str)
    threshold_time = published_time + timedelta(hours=24)
    now = datetime.now(timezone.utc)
    wait_seconds = (threshold_time - now).total_seconds()
    return wait_seconds

def main():
    vacancies_raw = get_vacancies()

    while True:
        HHStatistics.objects.all().delete()

        timestamps = []
        ios_vacancies = []

        for vac in vacancies_raw:
            details = get_vacancy_details(vac["id"])
            if is_ios_developer(details):
                ios_vacancies.append(details)

        for idx, details in enumerate(ios_vacancies, 1):
            name = details.get("name", "Без названия")
            description = details.get("description", "Нет описания")
            clean_description = re.sub(r'<[^>]+>', '', description)[:300] + '...'
            skills = details.get("key_skills", [])
            skills_str = ", ".join(skill["name"] for skill in skills) if skills else "Нет навыков"
            company = details.get("employer", {}).get("name", "Не указана компания")
            salary = format_salary(details.get("salary"))
            area = details.get("area", {}).get("name", "Не указан регион")
            published_at = details.get("published_at", "Не указана дата")
            published_at_dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            vacancy_url = details.get("alternate_url", "")
            timestamps.append(time_until_older_than_24h(published_at))

            if not HHStatistics.objects.filter(name=name, company=company, published_at=published_at_dt).exists():
                HHStatistics.objects.create(
                    name=name,
                    description=clean_description,
                    skills_str=skills_str,
                    company=company,
                    salary=salary,
                    area=area,
                    published_at=published_at_dt,
                    url=vacancy_url,
                )

            print(f"{idx}. Название вакансии: {name}")
            print(f"   Описание вакансии: {clean_description[:100]}...")
            print(f"   Навыки: {skills_str}")
            print(f"   Компания: {company}")
            print(f"   Оклад: {salary}")
            print(f"   Регион: {area}")
            print(f"   Дата публикации: {published_at_dt}\n")

        print(timestamps)
        time.sleep(min(timestamps))

if __name__ == "__main__":
    main()
