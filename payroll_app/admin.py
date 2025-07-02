from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Attendance, Salary

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model=CustomUser
    list_display=('username','email','phone_number','address','role')
admin.site.register(CustomUser,CustomUserAdmin) 
admin.site.register(Attendance)
admin.site.register(Salary)
   

