from django.db import models
from django.contrib.auth.models import User
from auth_system.models import EmployerProfile


#Міста
class City(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

#Категорій
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    

#Вакансій роботи
class Vacancy(models.Model):
    EMPLOYMENT_CHOICES = [
        ('full_time', 'Повна зайнятість'),
        ('part_time', 'Неповна зайнятість'),
    ]

    EXPERIENCE_CHOICES = [
        ('no_experience', 'Без досвіду'),
        ('experience', 'Досвід роботи'),
    ]

    WORK_FORMAT_CHOICES = [
        ('office', 'В офісі'),
        ('remote', 'Віддалено'),
        ('hybrid', 'Гібрид'),
    ]

    title = models.CharField(max_length=256)#Заголовок
    description = models.TextField()#опис
    description1 = models.TextField(null=True, blank=True)#опис
    description2 = models.TextField(null=True, blank=True)#опис
    link = models.URLField(max_length=500, null=True, blank=True)
    company = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name="vacancies")
    image = models.ImageField(upload_to='vacancies/images/',  null=True, blank=True)
    price_start = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_end = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default='full_time', verbose_name="Тип зайнятості")
    work_format = models.CharField(max_length=20, choices=WORK_FORMAT_CHOICES, default='office', verbose_name="Формат роботи")
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='no_experience', verbose_name="Досвід роботи")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name="vacancies", null=True)
    street = models.CharField(max_length=255, verbose_name="Вулиця")
    house_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Будинок / Офіс")
    date = models.DateTimeField(auto_now_add=True)#дата створення
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        ordering = ['-date']
        
    def total_applications(self):
        return self.applications.count()
    
    def __str__(self):
        return self.title
    
#Резюме користувача
class Resume(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resume")#автор
    title = models.CharField(max_length=256)#Заголовок
    description = models.TextField()#опис
    description1 = models.TextField(null=True, blank=True)#опис
    description2 = models.TextField(null=True, blank=True)#опис
    description3 = models.TextField(null=True, blank=True)#опис
    description4 = models.TextField(null=True, blank=True)#опис
    file = models.FileField(upload_to='resumes/',  null=True, blank=True)#файл   
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True,)#дата створення
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Дата оновлення")

    def __str__(self):
        return self.title
    
class Application(models.Model):
    STATUS_CHOICES = (
        ('under_review', 'На розгляді'),
        ('reject', 'Відхилено'),
        ('accepted', 'Прийнято'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    res_file = models.FileField(upload_to='application_docs/', null=True, blank=True) # Ось воно!
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='under_review')


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'vacancy'], name='unique_user_application')
        ]
        ordering = ['-created_at']

    
    def total_applications(self):
        return self.applications.count()

#Відгуки про сайт
class Response(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name="site_comment")#автор
    content = models.TextField()#опис
    date = models.DateTimeField(auto_now_add=True)#дата створення
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Відгук від {self.author.username}'
    


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','response')




#python manage.py runserver