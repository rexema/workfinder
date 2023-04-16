from django.urls import path
from django.views.generic import RedirectView
from jobapp import views

app_name = "jobapp"

urlpatterns = [
    path('', RedirectView.as_view(url="news/")),
    path('news/', views.NewsPageView.as_view(), name='news'),
    #path('news/detail/<int:id>/', ...),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('contacts/', views.ContactsPageView.as_view(), name='contacts'),
    path('', views.home_view, name='home'),
    path('jobs/create/', views.create_job_view, name='create-job'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
]
