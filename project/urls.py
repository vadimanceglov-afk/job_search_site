from django.urls import path
from . import views



urlpatterns = [
    path('', views.Job_ListView.as_view(), name='job_list'),
    path('job-site/', views.Job_site_ListView.as_view(), name='job_site'),
    path('job-detail/', views.Job_DetailView.as_view(), name='job_detail'),
    path('job-creat/', views.Job_CreateView.as_view(), name='job_creat'),

]