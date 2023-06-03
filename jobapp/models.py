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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Соискатель', related_name='resumes')

    title = models.CharField(default=None, max_length=255, verbose_name='Название резюме')
    photo = models.ImageField(null=True, blank=True, upload_to='images/', height_field=None, width_field=None,
                              max_length=100)
    name = models.CharField(blank=False, max_length=50, verbose_name='Имя')
    surname = models.CharField(blank=False, max_length=100, verbose_name='Фамилия')
    date_birth = models.DateField( verbose_name='Дата рождения',null=True, blank=True)
    home_town = models.CharField( verbose_name='Город, где вы проживаете', max_length=80,null=True, blank=True)
    phone_num = models.CharField( verbose_name='Номер телефона', max_length=50,null=True, blank=True)
    job_position = models.CharField( verbose_name='Желаемая должность', max_length=100,null=True, blank=True)
    salary = models.PositiveIntegerField( verbose_name='Желаемая заработная плата',null=True, blank=True)
    skills = models.CharField( verbose_name='Профессиональные навыки', max_length=100,null=True, blank=True)
    about_me = models.TextField(verbose_name='О себе',null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'


class Experience(models.Model):
    """
    Модель Опыт работы
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=None, verbose_name='Начало работы',null=True, blank=True)
    end_date = models.DateField(default=None, verbose_name='Окончание',null=True, blank=True)
    company = models.CharField(default=None, verbose_name='Организация', max_length=100)
    position = models.CharField(default=None, verbose_name='Должность', max_length=100)
    responsibilities = models.TextField(default=None, verbose_name='Обязанности')


class Education(models.Model):
    """
    Модель Образование
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.CharField(default=None, verbose_name='Учебное заведение', max_length=200)
    faculty = models.CharField(default=None, verbose_name='Факультет', max_length=200)
    specialization = models.CharField(default=None, verbose_name='Специализация', max_length=200)
    graduation_year = models.DateField(default=None, verbose_name='Год окончания')
