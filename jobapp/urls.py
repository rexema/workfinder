from django.urls import path
from jobapp import views

app_name = "jobapp"

urlpatterns = [

    path('', views.home_view, name='home'),
]
