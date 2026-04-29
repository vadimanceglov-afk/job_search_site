from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from .models import UserProfile, EmployerProfile

#перевірка ролі користувача
def role_view(request):
    pass

#Інфа про користувача
class Job_ProfileView(DetailView):
    pass

#Інфа про компанію
class Job_EmployerView(DetailView):
    pass

#Реєстрація нового користувача
class Job_singupView(CreateView):
    pass