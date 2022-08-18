from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect, render


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha_confirm = request.POST.get('senha_confirm')

    if (not nome 
        or not sobrenome 
        or not email 
        or not usuario 
        or not senha 
        or not senha_confirm):
        messages.error(request, 'Todos os campos precisam ser preenchidos.')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/register.html')

    if len(usuario) < 6:
        messages.error(request, 'Usuário deve ter no mínimo 6 caracteres.')
        return render(request, 'accounts/register.html')
    
    if len(senha) < 6:
        messages.error(request, 'Senha deve ter no mínimo 6 caracteres.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe.')
        return render(request, 'accounts/register.html')

    messages.add_message(request, messages.SUCCESS, 'Cadastrado com sucesso!')
    
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    
    user.save()
    
    return redirect('login')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
