from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager

GENDER = (
    ('M', "Male"),
    ('F', "Female"),
)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={'unique': 'Пользователь с таким email уже есть'}
    )
    role = models.CharField(choices=ROLE, max_length=10)
    gender = models.CharField(choices=GENDER, max_length=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = CustomUserManager()
