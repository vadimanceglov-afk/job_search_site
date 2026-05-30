from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from .models import UserProfile, EmployerProfile
from .forms import LoginForm, SignUp_UserForm, SignUp_EmployerForm
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from project.views import apply_for_job
from project.models import Application, Vacancy, Resume


def Choise(request):
    return render(request=request, template_name="auth_s/cho.html")


def user_logout(request):
    logout(request)
    return redirect("job_list")


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )

            if user and user.is_active:
                login(request, user)
                if UserProfile.objects.filter(user=user).exists():
                    return redirect('job_list')
                

                elif EmployerProfile.objects.filter(user=user).exists():
                    return redirect('job_company')
    else:
        form = LoginForm()

    return render(request, 'auth_s/login.html', {'form': form})


#Інфа про користувача
class Job_ProfileView(DetailView):
    model = UserProfile
    template_name = "auth_s/profile.html"
    context_object_name = 'profile'

    def get_object(self):
        obj, created = UserProfile.objects.get_or_create(user=self.request.user)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Resume.objects.filter(author=self.object.user)
        context['user_applications'] = Application.objects.filter(author=self.request.user)
        
        return context
    


#Інфа про компанію
class Job_EmployerView(DetailView):
    model = EmployerProfile
    template_name = "auth_s/profileM.html"
    context_object_name = "employer"
    
    def get_object(self, queryset=None):
        obj, created = EmployerProfile.objects.get_or_create(user=self.request.user)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(vacancy__company=self.object)
        context['jobs'] = Vacancy.objects.filter(company=self.object)
        
        return context

#Реєстрація нового користувача
class Job_singupView(CreateView):
    form_class = SignUp_UserForm
    template_name = 'auth_s/register.html'
    success_url = reverse_lazy('job_profile')

    def form_valid(self, form):
        user = form.save()

        f_name = form.cleaned_data.get('first_name')
        l_name = form.cleaned_data.get('last_name')
        p_name = form.cleaned_data.get('patronymic')
        date = form.cleaned_data.get('birth_date')
        ref = form.cleaned_data.get('referral')

        UserProfile.objects.create(
            user=user,
            first_name=f_name,
            last_name=l_name,
            patronymic=p_name,
            birth_date = date,
            referral = ref,
        )

        login(self.request, user)
        messages.success(self.request, 'Реєстрація успішна!')
        return redirect(self.success_url)


#Реєстрація нової компаній
class Job_Emp_singupView(CreateView):
    form_class = SignUp_EmployerForm
    template_name = 'auth_s/register_e.html'
    success_url = reverse_lazy('job_company')

    def form_valid(self, form):
        user = form.save()
        EmployerProfile.objects.create(
            user=user,
            employer_type=form.cleaned_data['employer_type'],
            name_company=form.cleaned_data.get('name_company'),
            description=form.cleaned_data.get('description'),
            referral_company=form.cleaned_data.get('referral_company'),
            website=form.cleaned_data.get('website')
        )

        login(self.request, user)
        return redirect(self.success_url)

#Редагувати профіль користувача
class Profile_UpdateView(UpdateView):
    model = UserProfile
    template_name = "auth_s/profile_form.html"
    fields = ['patronymic', 'gender', 'op'] # вкажи потрібні поля
    success_url = reverse_lazy('job_profile')

    def get_object(self):
        return self.request.user.profile
    
    def form_valid(self, form):
        messages.success(self.request, 'Профіль успішно оновлено!')
        return super().form_valid(form)
    
#Редагувати профіль компаній
class Company_UpdateView(UpdateView):
    model = EmployerProfile
    template_name = "auth_s/profile_form.html"
    fields = ['name_company', 'description', 'employer_type'] # вкажи потрібні поля
    success_url = reverse_lazy('job_company')

    def get_object(self, queryset=None):
        # Безпечно дістаємо профіль компанії поточного юзера
        obj, created = EmployerProfile.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'Дані компанії успішно оновлено!')
        return super().form_valid(form)

    def get_success_url(self):
        # Якщо твій урл 'job_company' не потребує id (бо бере юзера з request), залишай просто редірект.
        # Якщо потребує pk, цей метод динамічно передасть його туди:
        return reverse_lazy('job_company')