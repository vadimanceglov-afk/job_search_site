from django import forms
from project.models import Vacancy, Response, Resume, Application

class Vacancy_CreatFrom(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ["title", "description", 
                  "category", "link", 
                  "price_start", "price_end", 
                  "image", "city",
                  "street"]
        
        #widgets = {({})}

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


class Application_Form(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume", "res_file"]

class Vacancy_SurchFrom(forms.ModelForm):
    pass

class Vacancy_FilterFrom(forms.ModelForm):
    pass