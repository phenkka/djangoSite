FROM python:3.11

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . /app

# Установка зависимостей
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

# Команда запуска (может быть изменена в зависимости от среды)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]