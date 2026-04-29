from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Ч', 'Чоловік'),
        ('Ж', 'Жінка')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #
    first_name = models.CharField(max_length=100,blank=True, verbose_name='first_name')#імя
    last_name = models.CharField(max_length=100,blank=True, verbose_name='last_name')#прізвище
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name='patronymic')#по батькові
    birth_year = models.IntegerField(null=True, blank=True)#вік
    birth_date = models.DateField(null=True, blank=True)#дата народження
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, default='Ч')#стать
    bio = models.TextField(blank=True)#опис
    referral = models.ForeignKey('project.Category', on_delete=models.SET_NULL, null=True)#направлення

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"

class EmployerProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer')

    name_company = models.CharField(max_length=20)#назва компанії
    description = models.TextField()#опис
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)#логотип
    referral_company = models.ForeignKey('project.Category', on_delete=models.SET_NULL, null=True)#направлення компаній
    website = models.URLField(max_length=200, null=True, blank=True)#посилання на сайт компаній

    def __str__(self):
        return self.name_company