from django.urls import path
from . import views



urlpatterns = [
    path('', views.Job_ListView.as_view(), name='job_list'),
    path('job-site/', views.Job_site_ListView, name='job_site'),
    path('job-datail/<int:pk>/', views.Job_DetailView.as_view(), name='job_datail'),
    path('job-creat/', views.Job_CreateView.as_view(), name='job_creat'),
    path('like/response/<int:pk>/', views.Like_Response, name='Like_Response'),
]