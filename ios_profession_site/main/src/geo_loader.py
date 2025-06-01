import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import rcParams

# Настройки графиков
rcParams['font.family'] = 'Arial'
plt.style.use('seaborn-v0_8')

# Папка сохранения
output_folder = os.path.join('data', 'geo')
os.makedirs(output_folder, exist_ok=True)

# Ключевые слова для iOS-разработчиков
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
                salary_from = float(row['salary_from']) if row['salary_from'] else 0
                salary_to = float(row['salary_to']) if row['salary_to'] else 0

                if salary_from or salary_to:
                    salary = (salary_from + salary_to) / 2 if salary_to else salary_from

                    # Перевод валют
                    if row['salary_currency'] == 'USD':
                        salary *= 90
                    elif row['salary_currency'] == 'EUR':
                        salary *= 100
                    elif row['salary_currency'] not in ['RUR', 'RUB']:
                        continue

                    if salary > 10_000_000:
                        continue

                    data.append({
                        'area': row['area_name'],
                        'salary': salary
                    })
            except Exception as e:
                print(f"Ошибка: {e}")
                continue
    return pd.DataFrame(data)

try:
    file_path = 'data/vacancies_2024.csv'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    df = process_data(file_path)

    if df.empty:
        raise ValueError("Нет данных")

    total_vacancies = len(df)

    # 1. Уровень зарплат по городам (средняя зарплата, топ-10)
    salary_by_city = df.groupby('area')['salary'].mean().sort_values(ascending=False).head(10).reset_index()

    plt.figure(figsize=(12, 6))
    plt.barh(salary_by_city['area'], salary_by_city['salary'], color='green')
    plt.title('Уровень зарплат по городам для iOS-разработчиков', fontsize=14)
    plt.xlabel('Средняя зарплата, руб.', fontsize=12)
    plt.gca().invert_yaxis()
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'geo_ios_city_salary.png'), dpi=300)
    plt.close()

    salary_by_city.to_csv(os.path.join(output_folder, 'geo_ios_city_salary.csv'), index=False)

    # 2. Доля вакансий по городам (только города с долей > 1%)
    city_counts = df['area'].value_counts()
    city_share = (city_counts / total_vacancies).loc[lambda x: x > 0.01] * 100
    city_share = city_share.sort_values(ascending=False).reset_index()
    city_share.columns = ['area', 'share']
    city_share['share'] = city_share['share'].round(2)

    plt.figure(figsize=(12, 6))
    plt.barh(city_share['area'], city_share['share'], color='purple')
    plt.title('Доля вакансий по городам для iOS-разработчиков', fontsize=14)
    plt.xlabel('Доля вакансий, %', fontsize=12)
    plt.gca().invert_yaxis()
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'geo_ios_city_vacancy_share.png'), dpi=300)
    plt.close()

    city_share.to_csv(os.path.join(output_folder, 'geo_ios_city_vacancy_share.csv'), index=False)

except Exception as e:
    print(f"Ошибка: {e}")
