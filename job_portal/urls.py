from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('', include('jobapp.urls', namespace='jobapp')),
    # path('', include('parser.urls', namespace='parser')),
]
