from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .models import ContatoForm


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    if User.objects.filter(email=usuario).exists():
        usuario = User.objects.filter(email=usuario).first().username
        # usuario = User.objects.filter(email=usuario).get().username

    user = auth.authenticate(username=usuario, password=senha)
        
    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Logado com sucesso!')
        return redirect('dashboard')
    

def logout(request):
    auth.logout(request)
    messages.info(request, 'Sua sessão foi finalizada com sucesso!')
    return redirect('login')


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


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = ContatoForm
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = ContatoForm(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao cadastrar contato.')
        form = ContatoForm(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} cadastrado com sucesso!')
    return redirect('dashboard')
