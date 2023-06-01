from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from users import views


app_name = 'users'

urlpatterns = [

    path('employee/register/', views.employee_registration, name='employee-registration'),
    path('employer/register/', views.employer_registration, name='employer-registration'),
    path('profile/', views.ProfilePageView.as_view(), name='profile'),
    path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/resume/', views.resume_add, name='add-resume'),
    path('profile/resume/<int:id>/', views.show_resume, name='show-resume'),
    path('profile/resume/experience/', views.experience_add, name='add-experience'),
    path('profile/resume/education/', views.education_add, name='add-education'),
    path('resumes/', views.resume_list_view, name='resume-list'),
    path('resumes/<int:id>/', views.resume_single, name='resume-single'),
    path('resume/edit/<int:id>/', views.employee_edit_resume, name='edit-resume'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
