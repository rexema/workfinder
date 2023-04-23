from django.db import models
from django.utils import timezone

class Vacancy_Parsed(models.Model):
    """
    Модель Парсинга вакансий
    """
    title = models.CharField(max_length=250)
    salary = models.CharField(max_length=250)
    url = models.CharField(max_length=250, unique=True)
    name_company = models.CharField(max_length=250)
    adress_company = models.CharField(max_length=250)
    description  = models.TextField()
    key_skills = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_date']
   
    class Admin:
        pass


class Resume_Parsed(models.Model):
    """
    Модель Парсинга резюме
    """
    url = models.CharField(max_length=250, unique=True)
    title = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
   
    class Admin:
        pass