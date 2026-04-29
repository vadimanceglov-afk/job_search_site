from django.urls import path
from . import views

app_name = 'jobpr'

urlpatterns = [
    path('job-profil/', views.Job_ProfileView.as_view(), name='job_profil'),
    path('job-signup/', views.Job_singupView.as_view(), name='job_signup'),

]