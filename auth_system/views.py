from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from .models import UserProfile

#Інфа про користувача
class Job_atchView(DetailView):
    pass

#Реєстрація нового користувача
class Job_singupView(CreateView):
    pass