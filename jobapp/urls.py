from django.urls import path
from jobapp import views

app_name = "jobapp"

urlpatterns = [

    path('', views.home_view, name='home'),
    path('jobs/create/', views.create_job_view, name='create-job'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
]
