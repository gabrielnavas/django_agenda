from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User as UserDjango
from .usecases import RegisterUserUsecase, User


def login(request):
    return render(request, 'account/login.html')


def logout(request):
    return render(request, 'account/logout.html')


def register(request):
    if request.method != 'POST':
        return render(request, 'account/register.html')

    usercase = RegisterUserUsecase(
        validate_email=validate_email,
        user_repository=UserDjango.objects
    )
    try:
        user = User(
            name=request.POST.get('name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            password_confirmation=request.POST.get('password_confirmation'),
        )
        user = usercase.handle(user)
        MESSAGE_SUCCESS_LOGIN = 'Usuário registrado com sucesso. Agora realize o login.'
        messages.add_message(request, messages.SUCCESS, MESSAGE_SUCCESS_LOGIN)
        return redirect('login')
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)

    return render(request, 'account/register.html')


def dashboard(request):
    return render(request, 'account/dashboard.html')
