from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, View

#Інфа про сайт
class Job_site_ListView(ListView):
    pass

#Виводе всі вакансій
class Job_ListView(ListView):
    pass

#Інформація про вакансію
class Job_DetailView(DetailView):
    pass

#Створити вакансію
class Job_CreateView(CreateView):
    pass

#Видалити вакансію (може буде робитись автоматично)
class Job_DeleteView(DeleteView):
    pass