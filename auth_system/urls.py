from django.urls import path
from . import views

app_name = 'jobpr'

urlpatterns = [
    path('job-profil/', views.Job_ProfileView.as_view(), name='job_profil'),
    path('job-profilM/', views.Job_EmployerView.as_view(), name='job_company'),
    path('job-signupM/', views.Job_Emp_singupView.as_view(), name='job_signupM'),
    path('job-update/', views.Profile_UpdateView.as_view(), name='job_update'),
    path('job-signup/', views.Job_singupView.as_view(), name='job_signup'),

]