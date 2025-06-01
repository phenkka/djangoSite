import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from collections import defaultdict
import matplotlib.ticker as ticker
from matplotlib import rcParams
import numpy as np

# Настройки для matplotlib
rcParams['font.family'] = 'Arial'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

# Путь к папке для результатов (внутри data/)
output_folder = os.path.join('data', 'stats')
os.makedirs(output_folder, exist_ok=True)


# Функция для конвертации зарплаты в рубли
def convert_salary(row):
    if pd.isna(row['salary_from']) or pd.isna(row['salary_to']) or row['salary_currency'] == '':
        return None

    salary_from = float(row['salary_from']) if row['salary_from'] else 0
    salary_to = float(row['salary_to']) if row['salary_to'] else 0
    currency = row['salary_currency']

    # Среднее значение вилки зарплат
    salary = (salary_from + salary_to) / 2 if salary_to != 0 else salary_from

    # Курсы валют (примерные, нужно использовать актуальные курсы ЦБ)
    exchange_rates = {
        'USD': 90.0,
        'EUR': 100.0,
        'KZT': 0.2,
        'RUR': 1,
        'RUB': 1
    }

    # Конвертируем в рубли, если валюта известна
    if currency in exchange_rates:
        salary_rub = salary * exchange_rates[currency]
        # Игнорируем зарплаты > 10 млн рублей
        return salary_rub if salary_rub <= 10000000 else None
    return None


# Чтение данных из CSV
def read_csv_data(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Преобразуем дату в год
            try:
                date = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z')
                year = date.year
            except:
                year = None

            # Конвертируем зарплату
            salary_rub = convert_salary(row)

            # Получаем навыки
            skills = row['key_skills'].split('\n') if row['key_skills'] else []

            data.append({
                'year': year,
                'salary_rub': salary_rub,
                'area_name': row['area_name'],
                'skills': skills
            })
    return pd.DataFrame(data)


# Загрузка данных
df = read_csv_data('data/vacancies_2024.csv')

# Фильтрация данных
df = df[df['salary_rub'].notna() & df['year'].notna()]

# 1. Динамика уровня зарплат по годам
salary_by_year = df.groupby('year')['salary_rub'].mean().reset_index()

plt.figure(figsize=(10, 6))
plt.plot(salary_by_year['year'], salary_by_year['salary_rub'], marker='o')
plt.title('Динамика уровня зарплат по годам')
plt.xlabel('Год')
plt.ylabel('Средняя зарплата, руб')
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'salary_dynamics.png'))
plt.close()

# 2. Динамика количества вакансий по годам
vacancies_by_year = df['year'].value_counts().sort_index().reset_index()
vacancies_by_year.columns = ['year', 'count']

plt.figure(figsize=(10, 6))
plt.bar(vacancies_by_year['year'], vacancies_by_year['count'])
plt.title('Динамика количества вакансий по годам')
plt.xlabel('Год')
plt.ylabel('Количество вакансий')
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'vacancies_dynamics.png'))
plt.close()

# 3. Уровень зарплат по городам (топ 20)
city_salary = df.groupby('area_name')['salary_rub'].mean().sort_values(ascending=False).head(20).reset_index()

plt.figure(figsize=(12, 8))
plt.barh(city_salary['area_name'], city_salary['salary_rub'])
plt.title('Уровень зарплат по городам (Топ 20)')
plt.xlabel('Средняя зарплата, руб')
plt.ylabel('Город')
plt.gca().invert_yaxis()
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'salary_by_city.png'))
plt.close()

# 4. Доля вакансий по городам (топ 20)
city_share = df['area_name'].value_counts(normalize=True).head(20).reset_index()
city_share.columns = ['area_name', 'share']

plt.figure(figsize=(12, 8))
plt.pie(city_share['share'], labels=city_share['area_name'], autopct='%1.1f%%')
plt.title('Доля вакансий по городам (Топ 20)')
plt.savefig(os.path.join(output_folder, 'vacancies_share_by_city.png'))
plt.close()

# 5. ТОП-20 навыков по годам
all_skills = defaultdict(int)
for skills in df['skills']:
    for skill in skills:
        all_skills[skill] += 1

top_skills = pd.DataFrame.from_dict(all_skills, orient='index', columns=['count']).sort_values('count',
                                                                                               ascending=False).head(20)

plt.figure(figsize=(12, 8))
plt.barh(top_skills.index, top_skills['count'])
plt.title('ТОП-20 навыков')
plt.xlabel('Количество упоминаний')
plt.ylabel('Навык')
plt.gca().invert_yaxis()
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'top_skills.png'))
plt.close()

# Сохранение таблиц в CSV
salary_by_year.to_csv(os.path.join(output_folder, 'salary_by_year.csv'), index=False)
vacancies_by_year.to_csv(os.path.join(output_folder, 'vacancies_by_year.csv'), index=False)
city_salary.to_csv(os.path.join(output_folder, 'salary_by_city.csv'), index=False)
city_share.to_csv(os.path.join(output_folder, 'vacancies_share_by_city.csv'), index=False)
top_skills.to_csv(os.path.join(output_folder, 'top_skills.csv'), index=True)

print(f'Графики и таблицы сохранены в папку: {os.path.abspath(output_folder)}')