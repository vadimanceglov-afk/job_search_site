from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

#Вакансій роботи
class Vacancy(models.Model):

    title = models.CharField(max_length=256)#Заголовок
    description = models.TextField()#опис
    link = models.URLField(max_length=500, null=True, blank=True)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vacancies")
    image = models.ImageField(upload_to='vacancies/images/',  null=True, blank=True)
    price_start = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_end = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name="vacancies", null=True)
    street = models.CharField(max_length=255, verbose_name="Вулиця")
    date = models.DateTimeField(auto_now_add=True)#дата створення

    def total_likes(self):
        return self.likes.count()

#Резюме користувача
class Resume(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resume")#автор
    title = models.CharField(max_length=256)#Заголовок
    description = models.TextField()#опис
    file = models.FileField(upload_to='resumes/',  null=True, blank=True)#файл

#Відгуки про сайт
class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coments")#автор
    content = models.TextField()#опис
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment by {self.author.username}'
    
    def total_likes(self):
        return self.likes.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Цей рядок робить так, щоб один юзер міг лайкнути один матеріал лише 1 раз
        unique_together = [['user', 'vacancy'], ['user', 'response']]




#python manage.py runserver