from django.urls import path
from . import views



urlpatterns = [
    path('', views.Job_ListView.as_view(), name='job_list'),
    path('job-site/', views.Job_site_ListView, name='job_site'),
    path('job-datail/<int:pk>/', views.Job_DatailView.as_view(), name='job_datail'),
    path('job-creat/', views.Job_CreateView.as_view(), name='job_creat'),
    path('job-creat-resume/', views.Job_ResumeCreateView.as_view(), name='job_creat_resume'),
    path('like/response/<int:pk>/', views.Like_Response, name='Like_Response'),
    path('apply/<int:vacancy_id>/', views.apply_for_job, name='apply_for_job'),
]