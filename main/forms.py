from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, label='Тема')
    message = forms.CharField(widget=forms.Textarea, label='Сообщение')
    email = forms.EmailField(label='Ваш Email')