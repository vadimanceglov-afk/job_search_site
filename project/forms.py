from django import forms
from project.models import Vacancy, Response, Resume, Application, Category, City

class Vacancy_CreatFrom(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ["title", "description", "description1", "description2", "category", "link", 
                  "price_start", "price_end", "image", "city", "street"]
        # widgets МАЮТЬ бути всередині Meta (з правильним відступом)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть заголовок...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description1': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description2': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'price_start': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
        }

class Response_CreatFrom(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Додайте коментар',
            'rows': 4
        })}


class Resume_CreatFrom(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["title", "description", "file"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть заголовок вакансії...'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Додайте детальний опис обов’язків та вимог',
                'rows': 4
            })
        }


class Application_Form(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume", "res_file"]
        widgets = {
            'resume': forms.Select(attrs={
                'class': 'form-select',
                'style': 'border: 2px solid #ffc107;'  # Твій фірмовий жовтий акцент
            }),
            'res_file': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
        
    

class Vacancy_SurchFrom(forms.Form):
    q = forms.CharField(
        label='Search', 
        max_length=100, 
        required=False,  # Додай це, щоб можна було зайти на сторінку без запиту
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Пошук вакансій...'
        })
    )
class Vacancy_FilterFrom(forms.Form):
# Поля для вибору зі списку (ForeignKey)
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), 
        required=False,
        label="Місто",
        empty_label="Всі міста", # Додає порожній пункт спочатку
        widget=forms.Select(attrs={'class': 'form-select'}) # Для гарного стилю Bootstrap
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False,
        label="Категорія",
        empty_label="Всі категорії",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Поля для ручного введення ціни
    # ВАЖЛИВО: назви мають збігатися з тими, що у views.py (request.GET.get("..."))
    price_start = forms.IntegerField(
        required=False, 
        label="Ціна від",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Від'})
    )
    
    price_end = forms.IntegerField(
        required=False, 
        label="Ціна до",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'До'})
    )