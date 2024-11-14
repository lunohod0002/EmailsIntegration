from django.shortcuts import render

from .forms import LoginForm
from .models import User


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            print(login, password)
            if (User.objects.filter(login=login).exists() == False):
                User.objects.create(login=login, password=password)

            context = {'credentials': {'mail_pass': password, 'login': login, 'mail_name': 'mail.ru'}}
            return render(request, 'messages.html', context=context)

    return render(request, 'login.html', {'form': form})


def messages_view(request):
    return render(request, 'messages.html', context={'text': 'Hello World!'})
