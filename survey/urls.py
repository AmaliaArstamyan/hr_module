# survey/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .views import home
from . import views

app_name = 'survey'

urlpatterns = [
    # Registration
    path('register/', views.register, name='register'),

    # Login / Logout
    path('accounts/login/',
         LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True),
         name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Redirect after login
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),

    # Dashboards
    path('hr/dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('teamlead/dashboard/', views.teamlead_dashboard, name='teamlead_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Forms
    path('hr/create-form/', views.create_form, name='create_form'),
    path('form/<int:id>/fill/', views.fill_form, name='fill_form'),

    # Results & Charts
    path('results/', views.results_table, name='results_table'),
    path('charts/', views.results_charts, name='results_charts'),

    # Feedback
    path('send-feedback/', views.send_feedback, name='send_feedback'),
    path('', views.home, name='home'),
]
