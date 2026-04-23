from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, View
from .models import Vacancy, Like, Response, Resume


def toggle_like(request, model_type, item_id):
    if model_type == 'vacancy':
        item = get_object_or_404(Vacancy, pk=item_id)
        like, created = Like.objects.get_or_create(user=request.user, vacancy=item)
    else:
        item = get_object_or_404(Response, pk=item_id)
        like, created = Like.objects.get_or_create(user=request.user, response=item)

    if not created:
        # If it existed, delete it (unlike)
        like.delete()
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

#Інфа про сайт
def Job_site_ListView(request):
    return render(request=request, template_name="jobs/job_site.html")

#Виводе всі вакансій
class Job_ListView(ListView):
    model = Vacancy
    context_object_name = "jobs"
    template_name = "jobs/job_list.html"

    def get_context_data(self, **kwargs):
        # Отримуємо стандартний контекст (там уже є jobs)
        context = super().get_context_data(**kwargs)
        # Додаємо в цей же контекст список усіх відгуків
        context['all_responses'] = Response.objects.all()
        return context

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
    #form_class = Materials_CreateForm
    success_url = reverse_lazy("job_list")

#Створити резюме
class Job_ResumeCreateView(CreateView):
    model = Resume
    template_name = "jobs/job_creat.html"
    #form_class = Materials_CreateForm
    success_url = reverse_lazy("job_list")

#Видалити вакансію (може буде робитись автоматично)
class Job_DeleteView(DeleteView):
    model = Vacancy
    template_name = "jobs/job_delete.html"
    success_url = reverse_lazy("job_list")

    #@staticmethod
    #def all_resume():
    #    return Resume.objects.all()
