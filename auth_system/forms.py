from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, EmployerProfile, GENDER_CHOICES
from project.models import Category

class LoginForm(forms.Form):
    username = forms.CharField(label='Логін', 
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пороль', 
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class SignUp_UserForm(UserCreationForm):
    username = forms.CharField(label="Логін (або пошта)", help_text="Використовуйте для входу на сайт")
    patronymic = forms.CharField(label="По батькові", required=False)
    gender = forms.ChoiceField(label="Стать", choices=GENDER_CHOICES)

    birth_date = forms.DateField(label="Дата народження", help_text="В")
    referral = forms.ModelChoiceField(label="Звідки дізналися", queryset=Category.objects.all())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={             
                'class': 'form-control',
                'placeholder': 'y'
            }),

            'first_name': forms.TextInput(attrs={             
                'class': 'form-control',
                'placeholder': 'y'
            }),

            'last_name': forms.TextInput(attrs={             
                'class': 'form-control',
                'placeholder': 'y'
            }),

            'patronymic': forms.TextInput(attrs={             
                'class': 'form-control',
                'placeholder': 'y'
            }),

            'gender': forms.Select(attrs={             
                'class': 'form-control',
                'placeholder': 'y'
            }),

            
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'y'
            }),
        
            'referral': forms.Select(attrs={             
                'class': 'form-control',
                'placeholder': 'y'
            }),

            'email': forms.EmailInput(attrs={             
                'class': 'form-control',
                'placeholder': 'y'
            }),
        }


class SignUp_EmployerForm(UserCreationForm):
    username = forms.CharField(
        label="Логін",
        help_text="Використовуйте для входу на сайт",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логін'})
    )
    
    email = forms.EmailField(
        label='Електронна пошта',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'})
    )

    name_company = forms.CharField(
        label='Назва компанії',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва вашої фірми'})
    )

    description = forms.CharField(
        label='Опис компанії',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Чим займається компанія?'})
    )

    referral_company = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Напрямок компанії',
        empty_label="Оберіть категорію",
        widget=forms.Select(attrs={'class': 'form-select'}) # Для випадаючих списків краще form-select
    )

    website = forms.URLField(
        label='Сайт компанії',
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'})
    )
    
    employer_type = forms.ChoiceField(
        label='Тип реєстрації',
        choices=[('private', 'Приватна особа (Рекрутер)'), ('company', 'Компанія')],
        initial='private',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'employer_type', 'name_company', 'description', 'referral_company', 'website']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логін'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'company@mail.com'}),
        }

    # Валідація: якщо обрано "компанія", вимагаємо введення назви
    def clean(self):
        cleaned_data = super().clean()
        employer_type = cleaned_data.get('employer_type')
        name_company = cleaned_data.get('name_company')

        if employer_type == 'company' and not name_company:
            self.add_error('name_company', "Для типу реєстрації 'Компанія' це поле є обов'язковим.")
        return cleaned_data
