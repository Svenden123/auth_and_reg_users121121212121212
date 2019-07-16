from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render

from auth.forms import LoginForm, RegistrationForm


def home(request):
    return render(
        request,
        'home.html'
    )


def signup(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return render(request, 'accounts/signup_finish.html', {'form': user_form})
    else:
        user_form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active or True:
                    login(request, user)
                    return home(request)
                else:
                    return render(request, 'accounts/login.html', {'form': form, 'error': 'Аккаунт неактивен'})
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Не верный логин или пароль!'})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'accounts/logout.html')
