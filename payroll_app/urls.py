from django.urls import path
from .views import signup_view,login_view,logout_view,dashboard
from .import views
from django.urls import path
from . import views
urlpatterns = [
    path('signup/',signup_view,name='signup'),
    path('',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('dashboard/',dashboard,name="dashboard"),

    path('generate_salary/', views.generate_salary, name='generate_salary'),

    path('employee/delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),
    path('payslip/download/<int:salary_id>/', views.download_payslip, name='download_payslip'),
]





