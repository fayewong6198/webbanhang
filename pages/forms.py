from django import forms
from django.forms import ModelForm, Textarea, TextInput, PasswordInput
from .models import Contact


class ContactPageForm(ModelForm):
    error_css_class = "text-danger"

    class Meta:
        model = Contact
        fields = ('name', 'address', 'email', 'mobile', 'title', 'content')
        widgets = {
            'start_day': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }
