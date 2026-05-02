from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from .models import Vacancy, Like, Response, Resume, Application
from project.forms import Vacancy_CreatFrom, Response_CreatFrom, Resume_CreatFrom, Application_Form


@login_required
def apply_for_job(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    total_applications = Application.objects.filter(vacancy=vacancy).count()

    already_applied = Application.objects.filter(author=request.user, vacancy=vacancy).exists()
    if request.method == 'POST':
        if already_applied:
            messages.error(request, "You have already applied for this job.")
            return redirect('job_datail', vacancy_id=vacancy.id)
        else:
            form = Application_Form(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.vacancy = vacancy
                application.author = request.user
                if request.FILES.get('res_file'):
                    application.resume = None
                else:
                    if not application.resume:
                        application.resume = Resume.objects.filter(author=request.user).last()
                application.save()
                messages.success(request, "Application submitted successfully!")
                return redirect('job_list') 
    else:
        form = Application_Form()
        if 'resume' in form.fields:
            form.fields['resume'].queryset = Resume.objects.filter(author=request.user)
    
    return render(request, 'jobs/job_appl.html', {
        'form': form, 
        'already_applied': already_applied, 
        'total_applications': total_applications,
        'vacancy': vacancy
        })



def Like_Response(request, pk):
    response = get_object_or_404(Response, id=pk)
    like_qs = Like.objects.filter(user=request.user, response=response)
    if like_qs.exists():
        like_qs.delete()  # Забрати лайк
    else:
        Like.objects.create(user=request.user, response=response)     # Поставити лайк
    return redirect(request.META.get('HTTP_REFERER', '/'))

#Інфа про сайт
def Job_site_ListView(request):
    return render(request=request, template_name="jobs/job_site.html")

#Виводе всі вакансій
class Job_ListView(ListView):
    model = Vacancy
    form_class = Response_CreatFrom   
    context_object_name = "jobs"
    template_name = "jobs/job_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_responses'] = Response.objects.all()
        
        # Перевіряємо, чи юзер вже залишив відгук
        user_already_responded = False
        if self.request.user.is_authenticated:
            user_already_responded = Response.objects.filter(author=self.request.user).exists()
        
        context['user_already_responded'] = user_already_responded
        context['form'] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        # Обробка створення відгуку
        form = self.form_class(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.author = request.user
            response.save()
            return redirect('job_list') # Перезавантажуємо сторінку після успіху
        
        # Якщо форма невалідна, показуємо сторінку знову з помилками
        return self.get(request, *args, **kwargs)

#Інформація про вакансію
class Job_DatailView(DetailView):
    model = Vacancy
    context_object_name = "jobs"
    template_name = "jobs/job_datail.html"


#Інформація про вакансію
class Job_ResumeView(DetailView):
    model = Resume
    context_object_name = "resume"
    template_name = "jobs/job_resume.html"

#Редагувати вакансію
class Vacancy_UpdateView(UpdateView):
    model =Vacancy
    form_class = Vacancy_CreatFrom
    template_name = "jobs/job_creat.html"
    success_url = reverse_lazy("job_list")

#Створити вакансію
class Job_CreateView(CreateView):
    model = Vacancy
    template_name = "jobs/job_creat.html"
    form_class = Vacancy_CreatFrom
    success_url = reverse_lazy("job_list")

    def form_valid(self, form):
        # Перевірка, чи є користувач роботодавцем
        #if hasattr(self.request.user, 'employerprofile'):
            current_user = self.request.user
            form.instance.company = current_user.employer # або self.request.user.employerprofile /тут треба employerprofile/
            return super().form_valid(form)
        #else:
            #messages.error(self.request, "Тільки роботодавці можуть створювати вакансії")
            #return redirect('job_list')


#Створити резюме
class Job_ResumeCreateView(CreateView):
    model = Resume
    template_name = "jobs/job_creat_resume.html"
    form_class = Resume_CreatFrom
    success_url = reverse_lazy("job_list")

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.author = self.request.user 
        return super().form_valid(form)

#Видалити вакансію (може буде робитись автоматично)
class Job_DeleteView(DeleteView):
    model = Vacancy
    template_name = "jobs/job_delete.html"
    success_url = reverse_lazy("job_list")

    #@staticmethod
    #def all_resume():
    #    return Resume.objects.all()
