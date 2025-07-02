from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    phone_number=models.CharField(max_length=20)
    address=models.TextField()
    department=models.CharField(max_length=100)
    basic_salary=models.DecimalField(max_digits=10,decimal_places=3)
    role= models.CharField(max_length=20, choices=[
    ('admin', 'Admin'),
    ('employee', 'Employee')  
    
    
],default="admin")
    
class Attendance(models.Model):
    employee_name=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    time=models.DateTimeField(blank=True,null=True)
    status=models.CharField(max_length=20)
    
    def __str__(self):
        return self.employee_name.username
    
class Salary(models.Model):
    employee_name= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    present_days = models.IntegerField()
    absent_days = models.IntegerField()
    # total_working_days = models.IntegerField()
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    salary_amount = models.DecimalField(decimal_places=5,max_digits=10)
    generated_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.employee_name.username
    

    

    
    

    

    


