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

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'patronymic',  'gender', 'email']



class SignUp_EmployerForm(UserCreationForm):
    username = forms.CharField(label="Логін (або пошта)", help_text="Використовуйте для входу на сайт")    
    name_company = forms.CharField(label='Назва компанії', max_length=100)
    description = forms.CharField(label='Опис компанії', widget=forms.Textarea(attrs={'rows': 4}), required=False)
    referral_company = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        label='Напрямок компанії',
        empty_label="Оберіть категорію"
    )
    website = forms.URLField(label='Сайт компанії', required=False)
    email = forms.EmailField(label='Електронна пошта', required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
