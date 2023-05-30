import os
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')
django.setup()

from django.utils import timezone
from faker import Faker

from jobapp.models import User, Category, Job, Applicant, BookmarkJob, Resume, Experience, Education

fake = Faker()

# Создаем пользователей
for i in range(10):
    user = User.objects.create_user(email=fake.email(), password='password')

# Создаем категории
categories = ['IT', 'Маркетинг', 'Продажи', 'Финансы', 'HR']
for category in categories:
    Category.objects.create(name=category)

# Создаем вакансии
users = User.objects.all()
categories = Category.objects.all()
for i in range(20):
    job = Job.objects.create(
        user=random.choice(users),
        title=fake.job(),
        description=fake.text(),
        location=fake.city(),
        job_type=random.choice(['1', '2', '3']),
        category=random.choice(categories),
        salary=fake.random_int(min=1000, max=100000),
        company_name=fake.company(),
        company_description=fake.text(),
        url=fake.url(),
        is_published=True,
        is_closed=False,
        timestamp=timezone.now()
    )

# Создаем соискателей
for i in range(10):
    applicant = Applicant.objects.create(
        user=random.choice(users),
        job=random.choice(Job.objects.all()),
        timestamp=timezone.now()
    )

# Создаем закладки вакансий
for i in range(10):
    bookmark = BookmarkJob.objects.create(
        user=random.choice(users),
        job=random.choice(Job.objects.all()),
        timestamp=timezone.now()
    )

# Создаем резюме
for i in range(10):
    resume = Resume.objects.create(
        user=random.choice(users),
        title=fake.job(),
        photo=None,
        name=fake.first_name(),
        surname=fake.last_name(),
        date_birth=fake.date_of_birth(),
        home_town=fake.city(),
        phone_num=fake.phone_number(),
        job_position=fake.job(),
        salary=fake.random_int(min=1000, max=100000),
        skills=fake.text(),
        about_me=fake.text()
    )

# Создаем опыт работы
for i in range(10):
    experience = Experience.objects.create(
        user=random.choice(users),
        start_date=fake.date_between(start_date='-10y', end_date='today'),
        end_date=fake.date_between(start_date='-10y', end_date='today'),
        company=fake.company(),
        position=fake.job(),
        responsibilities=fake.text()
    )

# Создаем образование
for i in range(10):
    education = Education.objects.create(
        user=random.choice(users),
        university=fake.company(),
        faculty=fake.text(),
        specialization=fake.text(),
        graduation_year=fake.date_between(start_date='-10y', end_date='today')
    )
