from django.urls import path
from . import views



urlpatterns = [
    path('', views.Job_ListView.as_view(), name='job_list'),
    path('job-site/', views.Job_site_ListView, name='job_site'),
    path('job-datail/<int:pk>/', views.Job_DetailView.as_view(), name='job_datail'),
    path('job-creat/', views.Job_CreateView.as_view(), name='job_creat'),
    path('like/<str:model_type>/<int:item_id>/', views.toggle_like, name='toggle_like'),
]