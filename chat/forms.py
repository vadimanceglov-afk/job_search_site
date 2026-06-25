from django import forms
from chat.models import ChatMessage

class FormChat(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Напишить повідомлення',
            'rows': 2,  # Робимо поле акуратним, не дуже високим
            'style': 'resize: none;'  # Забороняємо розтягувати мишкою
        })}