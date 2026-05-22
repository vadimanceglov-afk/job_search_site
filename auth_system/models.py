from django.db import models
from datetime import date
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('User', 'Користувач'),
    ('Employer', 'Роботодавець'),
    ('Admin', 'Адміністратор'),
]

GENDER_CHOICES = [
    ('Men', 'Чоловік'),
    ('Women', 'Жінка')
]

class UserProfile(models.Model):
    OP_CHOICES = [
        ('Yes', 'Так'),
        ('No', 'Ні')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    avatar = models.ImageField(upload_to='imge_avatar', null=True, blank=True)
    op = models.CharField(choices=OP_CHOICES, max_length=20, default='Yes', null=True, blank=True)#
    first_name = models.CharField(max_length=100,blank=True, verbose_name='first_name')#імя
    last_name = models.CharField(max_length=100,blank=True, verbose_name='last_name')#прізвище
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name='patronymic')#по батькові
    birth_date = models.DateField(null=True, blank=True)#дата народження
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, default='Ч')#стать
    role = models.CharField(choices=ROLE_CHOICES, max_length=20, default='User')#
    bio = models.TextField(blank=True)#опис
    referral = models.ForeignKey('project.Category', on_delete=models.SET_NULL, null=True)#направлення
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефону")
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"
    
    @property
    def age(self):
        # Безпечний розрахунок віку. Якщо birth_date == None, код не впаде в Error.
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

class EmployerProfile(models.Model):
    TYPES_CHOICES = (
        ('private', 'Приватна особа'),
        ('company', 'Компанія'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer')

    employer_type = models.CharField(max_length=10, choices=TYPES_CHOICES, default='private')#тип роботодавця
    name_company = models.CharField(max_length=20)#назва компанії
    role = models.CharField(choices=ROLE_CHOICES, max_length=20, default='Employer')#роль
    description = models.TextField()#опис
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)#логотип
    referral_company = models.ForeignKey('project.Category', on_delete=models.SET_NULL, null=True)#направлення компаній
    hq_location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Головний офіс (Місто, Країна)")
    website = models.URLField(max_length=200, null=True, blank=True)#посилання на сайт компаній

    def __str__(self):
        return self.name_company