from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [

    path('employee/register/', views.employee_registration, name='employee-registration'),
    path('employer/register/', views.employer_registration, name='employer-registration'),
    path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
