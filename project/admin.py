from django.contrib import admin
from .models import Vacancy, Category, Like, Response, Resume, City
# Register your models here.

admin.site.register(Vacancy)

admin.site.register(Category)

admin.site.register(Like)

admin.site.register(Response)

admin.site.register(Resume)

admin.site.register(City)