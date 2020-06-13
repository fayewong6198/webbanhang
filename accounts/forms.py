from django import forms
from django.forms import ModelForm, Textarea, TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from .models import User


class RegisterForm(UserCreationForm):
    error_css_class = "text-danger"

    class Meta:
        model = User
        fields = ('username', 'email',  'password1', 'password2')

        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label="User name", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your usename'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'gender', 'mobile', 'address')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = '__all__'
