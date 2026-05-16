from django.urls import path
from . import views


urlpatterns = [
    path('job-profil/', views.Job_ProfileView.as_view(), name='job_profile'),
    path('job-profilM/', views.Job_EmployerView.as_view(), name='job_company'),
    path('job-update/', views.Profile_UpdateView.as_view(), name='job_updateR'),
    path('job-login/', views.login_user, name='job_login'),
    path("logout/", views.user_logout, name="logout"),
    path('signup/', views.Choise, name='signup_cho'),
    path('signup/user/', views.Job_singupView.as_view(), name='signup_user'),
    path('signup/employer/', views.Job_Emp_singupView.as_view(), name='signup_employer'),
]