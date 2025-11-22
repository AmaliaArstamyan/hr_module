# hr_module/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from survey.views import register

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login / Logout
    path('login/', LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Register page
    path('register/', register, name='register'),

    # Include survey app URLs (other URLs)
    path('', include('survey.urls')),
]
