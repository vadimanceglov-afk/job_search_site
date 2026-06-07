from django import forms
from project.models import Vacancy, Response, Resume, Application, Category, City, EMPLOYMENT_CHOICES, EXPERIENCE_CHOICES

class Vacancy_CreatFrom(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ["title", "description", "description1", "description2", "category", 
                  "experience", "employment_type", "work_format", "link", "price_start", 
                  "price_end", "image", "city", "street", "house_number"]
        # widgets МАЮТЬ бути всередині Meta (з правильним відступом)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть заголовок...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description1': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description2': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'work_format': forms.Select(attrs={'class': 'form-select'}),
            'experience': forms.Select(attrs={'class': 'form-select'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'price_start': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control',}),
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
        fields = ["title", "city", "phone_res", "description", "description1", "description2", "description3", "description4", "file"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть заголовок резюме...'
            }),

            'phone_res': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть номер телефону...'
            }),

            'city': forms.Select(attrs={'class': 'form-control'}),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Додайте детальний опис обов’язків та вимог',
                'rows': 4
            }),

            'description1': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Додайте детальний опис обов’язків та вимог',
                'rows': 4
            }),

            'description2': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Додайте детальний опис обов’язків та вимог',
                'rows': 4
            }),

            'description3': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Додайте детальний опис обов’язків та вимог',
                'rows': 4
            }),

            'description4': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Додайте детальний опис обов’язків та вимог',
                'rows': 4
            }),
        }


class Application_Form(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume", "res_file"]
        widgets = {
            'resume': forms.Select(attrs={
                'class': 'form-select',
                'style': 'form-control'  # Твій фірмовий жовтий акцент
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
            'placeholder': 'Пошук за вакансійями/ містом /сферою'
        })
    )
    # 2. Вибір міста (Динамічний з бази даних)
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label='Місто',
        required=False,
        empty_label='Усі міста',  # Перший порожній пункт
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # 3. Вибір категорії (Динамічний з бази даних)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категорія',
        required=False,
        empty_label='Усі сфери',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    employment_type = forms.ChoiceField(
        choices=EMPLOYMENT_CHOICES,
        label='Тип зайнятості',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    experience = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES,
        label='Досвід роботи',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # 6. Зарплата "ВІД" (число)
    price_start = forms.IntegerField(
        label='Зарплата від',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Від'
        })
    )
    
    # 7. Зарплата "ДО" (число)
    price_end = forms.IntegerField(
        label='Зарплата до',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'До'
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