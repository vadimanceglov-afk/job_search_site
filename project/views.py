from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from project_system import settings
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from .models import Vacancy, Like, Response, Resume, Application, Category, City
from auth_system.models import EmployerProfile, UserProfile
from project.forms import Vacancy_CreatFrom, Response_CreatFrom, Resume_CreatFrom, Application_Form, Vacancy_SurchFrom, Vacancy_FilterFrom
from django.contrib.auth.mixins import LoginRequiredMixin
from project.mixins import UserJob
from django.http import HttpResponseRedirect
from django.db.models import Q


def job_sursceh(request):
    search_form = Vacancy_SurchFrom(request.GET)
    filter_form = Vacancy_FilterFrom(request.GET)
    
    all_cities = City.objects.all()
    all_categories = Category.objects.all()
    vac = Vacancy.objects.all()

    query = request.GET.get("q")
    city_id = request.GET.get('city')
    cat_id = request.GET.get('category')
    ex_id = request.GET.get('experience')
    em_id = request.GET.get('employment_type')
    p_start = request.GET.get("price_start")
    p_end = request.GET.get("price_end")

    if query:
        vac = vac.filter(
            Q(category__name__icontains=query) |
            Q(title__icontains=query) |
            Q(company__name_company__icontains=query) 
        ).distinct()

    if city_id:
        vac = vac.filter(city_id=city_id)
    if cat_id:
        vac = vac.filter(category_id=cat_id)
    if ex_id:
        vac = vac.filter(experience_id=ex_id)
    if em_id:
        vac = vac.filter(employment_type_id=ex_id)
    if p_start:
        vac = vac.filter(price_start__gte=p_start)
    if p_end:
        vac = vac.filter(price_end__lte=p_end)

    return render(request, 'jobs/job_surh.html', {
        'vac': vac, 
        'search_form': search_form,
        'filter_form': filter_form,
        'cities': all_cities,
        'categories': all_categories,
        'query': query,
        'price_start': p_start,
        'price_end': p_end,
    })


@login_required
def apply_for_job(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    application = Application.objects.filter(
        author=request.user, 
        vacancy=vacancy
    ).first()

    application_a = Application.objects.filter(vacancy__company__user=request.user).order_by('-created_at')
    
    already_applied = application is not None

    if request.method == 'POST':
        subject = f"Новий відгук на вакансію: {vacancy.title}"
        message = f"Привіт! На твою вакансію '{vacancy.title}' відгукнувся користувач {request.user.username}.\nПеревір свій кабінет на сайті!"
        from_email = settings.EMAIL_HOST_USER  # Твоя пошта Gmail з settings.py
        recipient_list = [vacancy.company.email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False, # Якщо False, то у разі помилки Django покаже її в консолі
        )
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
                elif not application.resume:
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
        'total_applications': vacancy.applications.count(), 
        'application': application,  
        'application_a': application_a,       
        'vacancy': vacancy
    })

@login_required
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
        context['company_al'] = EmployerProfile.objects.all()
        context['latest_objects'] = Vacancy.objects.order_by('-date')[:3]
        user_already_responded = False
        if self.request.user.is_authenticated:
            user_already_responded = Response.objects.filter(author=self.request.user).exists()

        context['search_form'] = Vacancy_SurchFrom() 
        
        if self.request.user.is_authenticated:
            context['user_already_responded'] = user_already_responded

        context['response_form'] = self.form_class() 
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


#Інформація про резюме
class Job_ResumeView(DetailView):
    model = Resume
    context_object_name = "resume"
    template_name = "jobs/job_resume.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()
        context['profil'] = UserProfile.objects.all()
        # Якщо користувач - роботодавець, показуємо тільки його вакансії
        if self.request.user.is_authenticated and hasattr(self.request.user, 'employer'):
            # Фільтруємо заявки тільки по вакансіям цієї компанії
            context['applications'] = Application.objects.filter(
                resume=resume,
                vacancy__company=self.request.user.employer   
            ).select_related('vacancy')
        else:
            # Для кандидата або інших - можна показати порожньо або свої заявки
            context['applications'] = Application.objects.none()
        
        return context
    
#Редагувати резюме
class Resume_UpdateView(UpdateView):
    model =Resume
    form_class = Resume_CreatFrom
    template_name = "jobs/job_creat_resume.html"
    success_url = reverse_lazy("job_profile")


#Редагувати вакансію
class Vacancy_UpdateView(UpdateView):
    model =Vacancy
    form_class = Vacancy_CreatFrom
    template_name = "jobs/job_creat.html"
    success_url = reverse_lazy("job_list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.company.user != request.user:
            return redirect('job_list') 
            
        return super().get(request, *args, **kwargs)


#Створити вакансію
class Job_CreateView(CreateView):
    model = Vacancy
    template_name = "jobs/job_creat.html"
    form_class = Vacancy_CreatFrom
    success_url = reverse_lazy("job_list")

    def form_valid(self, form):
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ВИДАЛЯЄМО self.get_object(), бо об'єкта ще не існує!
        
        if self.request.user.is_authenticated:
            # Шукаємо заявку поточного юзера (кандидата)
            application = Application.objects.filter(
                author=self.request.user, 
                # vacancy__company__user=self.request.user # Це було б дивно, бо юзер не може подавати заявку сам собі
            ).first()
            
            context['appli'] = application
        return context
    

#Видалити вакансію (може буде робитись автоматично)
class Job_DeleteView(DeleteView):
    model = Vacancy
    template_name = "jobs/job_delete.html"
    success_url = reverse_lazy("job_list")


#Зміна статусу
class Job_StatusChangeView(View):
    def post(self, request, *args, **kwargs):
        appli = self.get_object()
        
        new_status = request.POST.get('status')
        if new_status in ['accepted', 'reject']:
            appli.status = new_status
            appli.save()
            subject = f"На вашу заявку відгукнулись"
            message = f"Статус заявки:{appli.get_status_display()}"
            from_email = settings.EMAIL_HOST_USER  # Твоя пошта Gmail з settings.py

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[appli.author.email],
                fail_silently=False, # Якщо False, то у разі помилки Django покаже її в консолі
            )
            messages.success(request, f"Статус змінено на: {appli.get_status_display()}")
        else:
            messages.error(request, "Невірний статус")
            
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    def get_object(self):
        appli_id = self.kwargs.get("pk")
        return get_object_or_404(Application, pk = appli_id)