from django.contrib import admin
from django.urls import path, include
from survey.views import (
    hr_dashboard,
    teamlead_dashboard,
    employee_dashboard,
    create_form,
    fill_form,
    results_table,
    results_charts,
    send_feedback,
    redirect_after_login,
    register,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include survey app URLs
    path('', include('survey.urls')),

    # Optional: if you want some direct paths here too
    path('register/', register, name='register'),
    path('redirect-after-login/', redirect_after_login, name='redirect_after_login'),

    # Dashboards
    path('hr/dashboard/', hr_dashboard, name='hr_dashboard'),
    path('teamlead/dashboard/', teamlead_dashboard, name='teamlead_dashboard'),
    path('employee/dashboard/', employee_dashboard, name='employee_dashboard'),

    # Forms
    path('hr/create-form/', create_form, name='create_form'),
    path('form/<int:id>/fill/', fill_form, name='fill_form'),

    # Survey results
    path('results/', results_table, name='results_table'),
    path('charts/', results_charts, name='results_charts'),

    # Feedback
    path('send-feedback/', send_feedback, name='send_feedback'),
]
