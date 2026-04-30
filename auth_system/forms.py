from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, EmployerProfile

class SignUp_UserForm(UserCreationForm):
    #class Meta:
    #    model = User
    #    fields = ['username', 'email', 'password1', 'password2']
#
    #def save(self, commit=True):
        pass

class SignUp_EmployerForm(UserCreationForm):
    pass