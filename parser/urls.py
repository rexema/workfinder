from django.urls import path
from parser.views import set_parser, parse_vacancy, show_vacancy

app_name = "parser"

urlpatterns = [
    path('parser/', set_parser, name="run_parser"),
    path('parser/parse_vacancy', parse_vacancy, name='parse_vacancy'),
    path('parser/show_vacancy', show_vacancy, name='show_vacancy')
]
