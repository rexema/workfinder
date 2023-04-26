from django.urls import path
from parserapp.views import set_parser, parse_vacancy, show_vacancy

app_name = "parserapp"

urlpatterns = [
    path('parserapp/', set_parser, name="run_parser"),
    path('parserapp/parse_vacancy', parse_vacancy, name='parse_vacancy'),
    path('parserapp/show_vacancy', show_vacancy, name='show_vacancy')
]
