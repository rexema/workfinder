from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()

JOB_TYPE = (
    ('1', "Полная занятость"),
    ('2', "Частичная занятость"),
    ('3', "Стажировка"),
)


class Category(models.Model):
    """
    Модель категорий
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Job(models.Model):
    """
    Модель вакансии
    """
    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    tags = TaggableManager()
    location = models.CharField(max_length=300)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    category = models.ForeignKey(Category, related_name='Category', on_delete=models.CASCADE)
    salary = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300)
    company_description = models.TextField()
    url = models.URLField(max_length=200)
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Applicant(models.Model):
    """
    Модель соискателя
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.title


class BookmarkJob(models.Model):
    """
    Модель закладок вакансий
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.title


class Resume(models.Model):
    """
    Модель резюме
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Соискатель', related_name='resumes')
    title = models.CharField(max_length=255, verbose_name='Название резюме')
    description = models.TextField(verbose_name='Описание')
    experience = models.TextField(verbose_name='Опыт работы')
    salary = models.PositiveIntegerField(verbose_name='Желаемая заработная плата')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
