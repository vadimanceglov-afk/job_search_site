from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, View
from .models import Vacancy, Like, Response, Resume
from project.forms import Vacancy_CreatFrom, Response_CreatFrom

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
class Job_DetailView(DetailView):
    model = Vacancy
    context_object_name = "jobs"
    template_name = "jobs/job_datail.html"

    #@staticmethod
    #def all_resume():
    #    return Resume.objects.all()

#Створити вакансію
class Job_CreateView(CreateView):
    model = Vacancy
    template_name = "jobs/job_creat.html"
    form_class = Vacancy_CreatFrom
    success_url = reverse_lazy("job_list")

    def form_valid(self, form):

        vacancy = form.save(commit=False)

        vacancy.company = self.request.user 

        return super().form_valid(form)


#Створити резюме
class Job_ResumeCreateView(CreateView):
    model = Resume
    template_name = "jobs/job_creat.html"
    form_class = Vacancy_CreatFrom
    success_url = reverse_lazy("job_list")

#Видалити вакансію (може буде робитись автоматично)
class Job_DeleteView(DeleteView):
    model = Vacancy
    template_name = "jobs/job_delete.html"
    success_url = reverse_lazy("job_list")

    #@staticmethod
    #def all_resume():
    #    return Resume.objects.all()
