from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from .models import UserProfile, EmployerProfile
from django.contrib import messages
from django.contrib.auth.models import User

#перевірка ролі користувача
def role_view(request):
    pass

#Інфа про користувача
class Job_ProfileView(DetailView):
    model = UserProfile
    context_object_name = "auth_s"
    template_name = "auth_s/profile.html"

    def get_object(self):
        return self.request.user.profile

#Інфа про компанію
class Job_EmployerView(DetailView):
    model = EmployerProfile
    context_object_name = "auth_s"
    template_name = "auth_s/profileM.html"

    def get_object(self):
        return self.request.user.employer

#Реєстрація нового користувача
class Job_singupView(CreateView):
    #form_class = SignUpForm
    template_name = 'auth_s/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        #user = form.save(commit=True)
        #login(self.request, user)  # Автоматичний вхід після реєстрації
        #messages.success(self.request, 'Реєстрація успішна!')
        #return super().form_valid(form)
        pass

#Реєстрація нової компаній
class Job_Emp_singupView(CreateView):
    #form_class = SignUpForm
    template_name = 'auth_s/register.html'
    success_url = reverse_lazy('profileM')

    def form_valid(self, form):
        #user = form.save(commit=True)
        #login(self.request, user)  # Автоматичний вхід після реєстрації
        #messages.success(self.request, 'Реєстрація успішна!')
        #return super().form_valid(form)
        pass

# Дозволяє користувачу редагувати власний профіль (біографію, аватар)
class Profile_UpdateView(UpdateView):
    #model = 
    #fields = ['bio']
    template_name = 'auth_s/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile