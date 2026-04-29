from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, EmployerProfile

class SignUp_UserForm(UserCreationForm):
    pass


class SignUp_EmployerForm(UserCreationForm):
    pass