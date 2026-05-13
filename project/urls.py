from django.urls import path
from . import views



urlpatterns = [
    path('', views.Job_ListView.as_view(), name='job_list'),
    path('job-site/', views.Job_site_ListView, name='job_site'),
    path('job-datail/<int:pk>/', views.Job_DatailView.as_view(), name='job_datail'),
    path('job-resume/<int:pk>/', views.Job_ResumeView.as_view(), name='job_resume'),
    path('job-creat/', views.Job_CreateView.as_view(), name='job_creat'),
    path('job-delete/<int:pk>/delete', views.Job_DeleteView.as_view(), name='job_delete'),
    path('job-creat-resume/', views.Job_ResumeCreateView.as_view(), name='job_creat_resume'),
    path('job-update/<int:pk>/', views.Vacancy_UpdateView.as_view(), name='job_update'),
    path('like/response/<int:pk>/', views.Like_Response, name='Like_Response'),
    path('apply/<int:vacancy_id>/', views.apply_for_job, name='apply_for_job'),
    path('search/', views.job_sursceh, name='job_surh'),
    path('complete/<int:pk>/', views.Job_CompleteView.as_view(), name='job_comp'),
]