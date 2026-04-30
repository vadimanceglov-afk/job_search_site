from django.contrib import admin
from .models import UserProfile, EmployerProfile

admin.site.register(EmployerProfile)
admin.site.register(UserProfile)