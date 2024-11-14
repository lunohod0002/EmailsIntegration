from django import forms\

class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'login'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'password'}))

