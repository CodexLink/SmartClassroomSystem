from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .externs.subject_types import RoleDeclaredTypes
from .models import UserDataCredentials
from django.contrib.auth.forms import AuthenticationForm

class UserAuthForm(AuthenticationForm):
    class Meta:
        model = UserDataCredentials
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationUsername', 'placeholder': 'Required'}),
            'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'validationPassword', 'placeholder': 'Required'}),
        }
    username = forms.CharField(min_length=2, max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'validationUsername', 'placeholder': 'Required'}))
    password = forms.CharField(min_length=2, max_length=128, required=True, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'validationPassword', 'placeholder': 'Required'}))
