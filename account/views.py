from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User as UserDjango
from django.contrib.auth.decorators import login_required

from .usecases.register import RegisterUserUsecase, User


def login(request):
    if request.method != 'POST':
        return render(request, 'account/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user_found = UserDjango.objects.get(
            username=username, password=password)
        auth.login(request, user_found)
        MESSAGE_SUCCESS_LOGIN = 'Você fez login com sucesso.'
        messages.add_message(request, messages.SUCCESS, MESSAGE_SUCCESS_LOGIN)
        return redirect('dashboard')
    except:
        MESSAGE_WRONG_LOGIN = 'Nome de usuário ou senha invalidos.'
        messages.add_message(request, messages.ERROR, MESSAGE_WRONG_LOGIN)
        return render(request, 'account/login.html')


def logout(request):
    auth.logout(request)
    return redirect('dashboard')


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
        usercase.handle(user)
        MESSAGE_SUCCESS_LOGIN = 'Usuário registrado com sucesso. Agora realize o login.'
        messages.add_message(request, messages.SUCCESS, MESSAGE_SUCCESS_LOGIN)
        return redirect('login')
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)

    return render(request, 'account/register.html')


@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'account/dashboard.html')
