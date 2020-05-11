from django import forms
from .models import UserDataCredentials
from django.contrib.auth.forms import AuthenticationForm


class UserAuthForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = UserDataCredentials
        fields = ["username", "password"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "validationUsername",
                    "placeholder": "Required",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "type": "password",
                    "class": "form-control",
                    "id": "validationPassword",
                    "placeholder": "Required",
                }
            ),
        }

    username = forms.CharField(
        min_length=2,
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "validationUsername",
                "placeholder": "Required",
            }
        ),
    )
    password = forms.CharField(
        min_length=2,
        max_length=128,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "id": "validationPassword",
                "placeholder": "Required",
            }
        ),
    )
