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
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name="vacancies", null=True)
    street = models.CharField(max_length=255, verbose_name="Вулиця")
    date = models.DateTimeField(auto_now_add=True)#дата створення

    def total_applications(self):
        return self.applications.count()
    
    def __str__(self):
        return self.title
    
#Резюме користувача
class Resume(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resume")#автор
    title = models.CharField(max_length=256)#Заголовок
    description = models.TextField()#опис
    file = models.FileField(upload_to='resumes/',  null=True, blank=True)#файл   

    def __str__(self):
        return self.title
    
class Application(models.Model):
    STATUS_CHOICES = (
        ('reject', 'Відхилено'),
        ('under_review', 'На розгляді'),
        ('accepted', 'Прийнято'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    res_file = models.FileField(upload_to='application_docs/', null=True, blank=True) # Ось воно!
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'vacancy'], name='unique_user_application')
        ]

    def __str__(self):
        name = self.author.username if self.author else "Анонім"
        target = self.vacancy.title if self.vacancy else "невідому вакансію"
        return f"Заявка від {name} на {target}"
    
    def total_applications(self):
        return self.applications.count()

#Відгуки про сайт
class Response(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name="site_comment")#автор
    content = models.TextField()#опис
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