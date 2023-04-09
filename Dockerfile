# Указываем базовый образ
FROM python:3.8-slim-buster

# Устанавливаем переменную окружения для Python в режим отладки
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

# Устанавливаем зависимости для PostgreSQL и библиотек для Python
RUN apt-get update \
    && apt-get install libpq-dev \
    && apt-get install -y postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Копируем код приложения в контейнер
COPY . /app
WORKDIR /app

# Запускаем миграции и собираем статические файлы приложения
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

# Определяем порт, который будет использоваться для взаимодействия с контейнером
EXPOSE 8000

# Запускаем команду для запуска приложения внутри контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
