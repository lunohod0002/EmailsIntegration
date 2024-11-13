from django import forms
from .models import User  # импортируйте вашу модель


class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'login'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'password'}))

