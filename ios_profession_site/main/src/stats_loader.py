import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict, Counter
from matplotlib import rcParams
import requests
import xml.etree.ElementTree as ET

rcParams['font.family'] = 'Arial'
plt.style.use('seaborn-v0_8')

output_folder = os.path.join('data', 'statistics')
os.makedirs(output_folder, exist_ok=True)

CURRENCIES = ['USD', 'EUR', 'RUB', 'RUR', 'KZT', 'UAH', 'BYR', 'BYN', 'AZN', 'GBP']

course_cache = {}

def get_exchange_rate(date_str, currency):
    date_obj = datetime.strptime(date_str[:10], '%Y-%m-%d')
    first_day = date_obj.replace(day=1)
    date_key = first_day.strftime('%Y-%m-%d')
    if currency in ['RUB', 'RUR']:
        return 1.0
    if (date_key, currency) in course_cache:
        return course_cache[(date_key, currency)]
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={first_day.strftime('%d/%m/%Y')}"
    try:
        response = requests.get(url, timeout=5)
        response.encoding = 'windows-1251'
        root = ET.fromstring(response.text)
        rate = None
        for valute in root.findall('Valute'):
            code = valute.find('CharCode').text
            if code == currency:
                nominal = int(valute.find('Nominal').text)
                value_str = valute.find('Value').text
                value_float = float(value_str.replace(',', '.'))
                rate = value_float / nominal
                break
        course_cache[(date_key, currency)] = rate
        return rate
    except Exception:
        course_cache[(date_key, currency)] = None
        return None

def parse_salary(row):
    try:
        salary_from = float(row['salary_from']) if row['salary_from'] else 0
    except:
        salary_from = 0
    try:
        salary_to = float(row['salary_to']) if row['salary_to'] else 0
    except:
        salary_to = 0
    if salary_from == 0 and salary_to == 0:
        return None
    if salary_to:
        salary = (salary_from + salary_to) / 2
    else:
        salary = salary_from
    return salary

def process_data(file_path):
    salaries_by_year = defaultdict(list)
    vacancies_by_year = defaultdict(int)
    salaries_by_city = defaultdict(list)
    vacancies_by_city = defaultdict(int)
    skills_by_year = defaultdict(list)
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row['published_at']
            city = row['area_name'] if row['area_name'] else 'Не указан'
            currency = row['salary_currency'] if row['salary_currency'] else 'RUB'
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
                year = date_obj.year
            except Exception:
                continue
            vacancies_by_year[year] += 1
            vacancies_by_city[city] += 1
            salary = parse_salary(row)
            if salary is not None:
                rate = get_exchange_rate(date_str, currency)
                if rate is None:
                    continue
                salary_rub = salary * rate
                if salary_rub <= 10_000_000:
                    salaries_by_year[year].append(salary_rub)
                    salaries_by_city[city].append(salary_rub)
            key_skills = row['key_skills'].strip() if row['key_skills'] else ''
            if key_skills:
                skills = [s.strip() for s in key_skills.split('\n') if s.strip()]
                skills_by_year[year].extend(skills)

    salary_trend_data = []
    for y in sorted(salaries_by_year.keys()):
        avg_salary = sum(salaries_by_year[y]) / len(salaries_by_year[y]) if salaries_by_year[y] else 0
        salary_trend_data.append({'year': y, 'avg_salary': avg_salary})
    salary_trend_df = pd.DataFrame(salary_trend_data)

    vacancies_year_data = [{'year': y, 'count': vacancies_by_year[y]} for y in sorted(vacancies_by_year.keys())]
    vacancies_year_df = pd.DataFrame(vacancies_year_data)

    salary_city_data = []
    for c in salaries_by_city.keys():
        if len(salaries_by_city[c]) > 0:
            avg_salary = sum(salaries_by_city[c]) / len(salaries_by_city[c])
            salary_city_data.append({'city': c, 'avg_salary': avg_salary})
    salary_city_df = pd.DataFrame(salary_city_data).sort_values(by='avg_salary', ascending=False)

    total_vacancies = sum(vacancies_by_city.values())
    vacancies_city_data = [{'city': c, 'vacancy_share': vacancies_by_city[c]/total_vacancies} for c in vacancies_by_city.keys()]
    vacancies_city_df = pd.DataFrame(vacancies_city_data).sort_values(by='vacancy_share', ascending=False)

    skill_table_data = []
    for y in sorted(skills_by_year.keys()):
        counter = Counter(skills_by_year[y])
        top_20 = counter.most_common(20)
        for skill, count in top_20:
            skill_table_data.append({'year': y, 'skill': skill, 'count': count})
    skills_df = pd.DataFrame(skill_table_data)
    skills_df = skills_df.sort_values(['year', 'count'], ascending=[True, False])

    salary_trend_df.to_csv(os.path.join(output_folder, 'salary_dynamics.csv'), index=False)
    vacancies_year_df.to_csv(os.path.join(output_folder, 'vacancies_dynamics.csv'), index=False)
    salary_city_df.to_csv(os.path.join(output_folder, 'salary_by_city.csv'), index=False)
    vacancies_city_df.to_csv(os.path.join(output_folder, 'vacancies_share_by_city.csv'), index=False)
    skills_df.to_csv(os.path.join(output_folder, 'top_skills.csv'), index=False)

    plt.figure(figsize=(12,6))
    plt.plot(salary_trend_df['year'], salary_trend_df['avg_salary'], marker='o', linewidth=2)
    plt.title('Динамика уровня зарплат по годам', fontsize=14)
    plt.xlabel('Год', fontsize=12)
    plt.ylabel('Средняя зарплата, руб.', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_folder, 'salary_dynamics.png'), dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(12,6))
    plt.bar(vacancies_year_df['year'], vacancies_year_df['count'], color='orange', alpha=0.7)
    plt.title('Динамика количества вакансий по годам', fontsize=14)
    plt.xlabel('Год', fontsize=12)
    plt.ylabel('Количество вакансий', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_folder, 'vacancies_dynamics.png'), dpi=300, bbox_inches='tight')
    plt.close()

    top_20_cities_salary = salary_city_df.head(20)
    plt.figure(figsize=(14,8))
    plt.barh(top_20_cities_salary['city'][::-1], top_20_cities_salary['avg_salary'][::-1], color='green', alpha=0.7)
    plt.title('Уровень зарплат по городам (топ-20)', fontsize=14)
    plt.xlabel('Средняя зарплата, руб.', fontsize=12)
    plt.ylabel('Город', fontsize=12)
    plt.grid(True, axis='x', alpha=0.3)
    plt.savefig(os.path.join(output_folder, 'salary_by_city.png'), dpi=300, bbox_inches='tight')
    plt.close()

    top_20_cities_vac = vacancies_city_df.head(20)
    plt.figure(figsize=(14,8))
    plt.barh(top_20_cities_vac['city'][::-1], top_20_cities_vac['vacancy_share'][::-1], color='purple', alpha=0.7)
    plt.title('Доля вакансий по городам (топ-20)', fontsize=14)
    plt.xlabel('Доля вакансий', fontsize=12)
    plt.ylabel('Город', fontsize=12)
    plt.grid(True, axis='x', alpha=0.3)
    plt.savefig(os.path.join(output_folder, 'vacancies_share_by_city.png'), dpi=300, bbox_inches='tight')
    plt.close()

    if not skills_df.empty:
        top_skills = skills_df.groupby('skill')['count'].sum().sort_values(ascending=False).head(10).index.tolist()
        pivot_df = skills_df[skills_df['skill'].isin(top_skills)].pivot(index='year', columns='skill', values='count').fillna(0)
        plt.figure(figsize=(14, 8))
        for skill in pivot_df.columns:
            plt.plot(pivot_df.index, pivot_df[skill], marker='o', label=skill)
        plt.title('Динамика популярности ТОП-10 навыков', fontsize=14)
        plt.xlabel('Год', fontsize=12)
        plt.ylabel('Частота упоминаний', fontsize=12)
        plt.legend(title='Навык', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, 'top_skills.png'), dpi=300)
        plt.close()

process_data('data/vacancies_2024.csv')
