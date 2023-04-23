from django.contrib import admin

# Register your models here.
from parser.models import Vacancy_Parsed, Resume_Parsed

admin.site.register(Vacancy_Parsed)
admin.site.register(Resume_Parsed)
