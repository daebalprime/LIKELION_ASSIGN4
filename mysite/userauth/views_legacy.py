from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

from .forms import LoginForm, SignupForm
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from .forms import LoginForm, SignupForm

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(
                username=username,
                password=password
            )

            if user:
                django_login(request, user)
                return redirect('post:post_list')
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()
        # login_form = LoginForm(), SignupForm
    context = {
        'login_form': login_form,
    }
    return render(request, 'userauth/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.signup()
            return redirect('post:post_list')
    else:
        signup_form = SignupForm()

    context = {
        'signup_form': signup_form,
    }
    return render(request, 'member/signup.html', context)
