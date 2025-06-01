import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import rcParams

# Настройки для графиков
rcParams['font.family'] = 'Arial'
plt.style.use('seaborn-v0_8')

# Папка для сохранения результатов
output_folder = os.path.join('data', 'demand')
os.makedirs(output_folder, exist_ok=True)

# Ключевые слова для iOS-разработчика
profession_keywords = ['ios', 'apple', 'разработчик ios', 'ios developer']

def is_ios_vacancy(title):
    title = title.lower()
    return any(keyword in title for keyword in profession_keywords)

def process_data(file_path):
    data = []
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not is_ios_vacancy(row['name']):
                continue

            try:
                year = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z').year
                salary_from = float(row['salary_from']) if row['salary_from'] else 0
                salary_to = float(row['salary_to']) if row['salary_to'] else 0

                if salary_from or salary_to:
                    salary = (salary_from + salary_to) / 2 if salary_to else salary_from
                    # Курсы валют
                    if row['salary_currency'] == 'USD':
                        salary *= 90
                    elif row['salary_currency'] == 'EUR':
                        salary *= 100
                    elif row['salary_currency'] not in ['RUR', 'RUB']:
                        continue  # пропускаем незнакомые валюты

                    if salary > 10_000_000:
                        continue  # фильтр выбросов

                    data.append({'year': year, 'salary': salary})
            except Exception as e:
                print(f"Ошибка обработки строки: {e}")
                continue
    return pd.DataFrame(data)

try:
    if not os.path.exists('data/vacancies_2024.csv'):
        raise FileNotFoundError("ошибка")

    df = process_data('data/vacancies_2024.csv')

    if df.empty:
        raise ValueError("Нет данных")

    # 1. Динамика уровня зарплат по годам
    salary_trend = df.groupby('year')['salary'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    plt.plot(salary_trend['year'], salary_trend['salary'], marker='o', linewidth=2, color='blue')
    plt.title('Динамика уровня зарплат iOS-разработчиков по годам', fontsize=14)
    plt.xlabel('Год', fontsize=12)
    plt.ylabel('Средняя зарплата, руб.', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_folder, 'ios_salary_level_trend.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Динамика количества вакансий по годам
    vacancies_trend = df['year'].value_counts().sort_index().reset_index()
    vacancies_trend.columns = ['year', 'vacancies_count']
    plt.figure(figsize=(12, 6))
    plt.bar(vacancies_trend['year'], vacancies_trend['vacancies_count'], color='orange', alpha=0.7)
    plt.title('Динамика количества вакансий iOS-разработчиков по годам', fontsize=14)
    plt.xlabel('Год', fontsize=12)
    plt.ylabel('Количество вакансий', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_folder, 'ios_vacancies_count_trend.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Сохраняем таблицы CSV
    salary_trend.to_csv(os.path.join(output_folder, 'ios_salary_level_trend.csv'), index=False)
    vacancies_trend.to_csv(os.path.join(output_folder, 'ios_vacancies_count_trend.csv'), index=False)


except FileNotFoundError as e:
    print(f"Ошибка: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
