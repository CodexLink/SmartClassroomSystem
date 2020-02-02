from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .externs.subject_types import RoleDeclaredTypes

class UserAuthForm(forms.Form):
    username = forms.CharField(min_length=2, max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'validationUsername', 'placeholder': 'Required'}))
    password = forms.CharField(min_length=2, max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'validationPassword', 'placeholder': 'Required'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
