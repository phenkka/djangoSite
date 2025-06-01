import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict, Counter
from matplotlib import rcParams

# Настройки
rcParams['font.family'] = 'Arial'
plt.style.use('seaborn-v0_8')

# Папка для сохранения
output_folder = os.path.join('data', 'skills')
os.makedirs(output_folder, exist_ok=True)

# Ключевые слова для фильтрации
profession_keywords = ['ios', 'apple', 'разработчик ios', 'ios developer']

def is_ios_vacancy(title):
    title = title.lower()
    return any(keyword in title for keyword in profession_keywords)

def extract_skills_by_year(file_path):
    skills_by_year = defaultdict(list)

    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not is_ios_vacancy(row['name']):
                continue

            key_skills = row['key_skills'].strip()
            if not key_skills:
                continue

            try:
                year = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z').year
            except Exception:
                continue

            skills = [s.strip() for s in key_skills.split('\n') if s.strip()]
            skills_by_year[year].extend(skills)

    return skills_by_year

try:
    file_path = 'data/vacancies_2024.csv'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    skills_by_year = extract_skills_by_year(file_path)

    if not skills_by_year:
        raise ValueError("Нет данных по навыкам для iOS-разработчиков!")

    all_top_skills = set()
    table_data = []

    # Формирование таблицы: топ-20 навыков по годам
    for year in sorted(skills_by_year.keys()):
        counter = Counter(skills_by_year[year])
        top_20 = counter.most_common(20)

        for skill, count in top_20:
            all_top_skills.add(skill)
            table_data.append({
                'year': year,
                'skill': skill,
                'count': count
            })

    df = pd.DataFrame(table_data)
    df.sort_values(by=['year', 'count'], ascending=[True, False], inplace=True)
    df.to_csv(os.path.join(output_folder, 'skills_top_ios_trend.csv'), index=False)

    # Построим график для ТОП-10 навыков по суммарной частоте
    top_skills = df.groupby('skill')['count'].sum().sort_values(ascending=False).head(10).index.tolist()

    pivot_df = df[df['skill'].isin(top_skills)].pivot(index='year', columns='skill', values='count').fillna(0)

    plt.figure(figsize=(14, 8))
    for skill in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[skill], marker='o', label=skill)

    plt.title('Динамика популярности ТОП-10 навыков iOS-разработчика', fontsize=14)
    plt.xlabel('Год', fontsize=12)
    plt.ylabel('Частота упоминаний', fontsize=12)
    plt.legend(title='Навык', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'skills_top_ios_trend.png'), dpi=300)
    plt.close()


except Exception as e:
    print(f"Ошибка: {e}")
