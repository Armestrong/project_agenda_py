from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request, 'tmpl_accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    # checando usuario e senha
    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha invalidos')
        return render(request, 'tmpl_accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login sucedido')
        return redirect('dashboard')  # evita erro de reload da pagina


def logout(request):
    auth.logout(request)
    return redirect('dashboard')


def register(request):
    if request.method != 'POST':
        return render(request, 'tmpl_accounts/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    # Validando campo vazio
    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.info(request, 'Nenhum campo pode estar vazio.')
        return render(request, 'tmpl_accounts/register.html')

    # Validando usuario
    if len(usuario) < 6:
        messages.error(request, 'O usuario precisa ter mais de seis caracteres')
        return render(request, 'tmpl_accounts/register.html')

    # Validando senha
    if len(senha) < 2:
        messages.error(request, 'A senha precisa ter mais de seis caracteres')
        return render(request, 'tmpl_accounts/register.html')

    # Validando confirmação da senha
    if senha != senha2:
        messages.error(request, 'Por favor digite ambas as senha corretamente')
        return render(request, 'tmpl_accounts/register.html')

        # Validando email
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email incorreto')
        return render(request, 'tmpl_accounts/register.html')

    # Vertificando a existencia do mesmo email
    if User.objects.filter(first_name=nome).exists():
        messages.error(request, 'Usuario ja existe')
        return render(request, 'tmpl_accounts/register.html')

    # Vertificando a existencia do mesmo email
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email ja existe')
        return render(request, 'tmpl_accounts/register.html')

    messages.success(request, 'Cadastrado! Aproveite a experiencia !')
    user = User.objects.create_user(first_name=nome, last_name=sobrenome, email=email, username=usuario, password=senha)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')  # só deixa acessar essa pagina se o login estiver efetuado
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'tmpl_accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)
    if not form.is_valid():
        messages.error('Erro ao enviar o formulário.')
        form = FormContato(request.POST)
        return render(request, 'tmpl_accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')
    if len(descricao) < 5:
        messages.error(request, 'Descrição precisa ter mais de 5 caracteres')
        form = FormContato(request.POST)
        return render(request, 'tmpl_accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso!')
    return redirect('dashboard')