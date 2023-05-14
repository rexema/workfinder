from django.urls import path
from django.views.generic import RedirectView
from jobapp import views

app_name = "jobapp"

urlpatterns = [
    path('', RedirectView.as_view(url="news/")),
    path('jobs/', views.job_list_view, name='job-list'),
    path('jobs/create/', views.create_job_view, name='create-job'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('bookmark-job/<int:id>/', views.job_bookmark_view, name='bookmark-job'),
    path('news/', views.NewsPageView.as_view(), name='news'),
    #path('news/detail/<int:id>/', ...),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('contacts/', views.ContactsPageView.as_view(), name='contacts'),
    path('', views.home_view, name='home'),
    path('result/', views.search_result_view, name='search_result'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/job/edit/<int:id>', views.job_edit_view, name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_job_view, name='complete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
]
