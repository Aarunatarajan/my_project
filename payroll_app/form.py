from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser

class CustomUserSignupForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','email','phone_number','role','password1','password2','department','basic_salary']
class CustomUserLoginForm(AuthenticationForm):
    username=forms.CharField(label="Username")    
    password=forms.CharField(widget=forms.PasswordInput) 
        
        