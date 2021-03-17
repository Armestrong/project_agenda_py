from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.validators import validate_email

from django.contrib.auth.decorators import login_required
from .models import FormContato
from django.core.exceptions import ValidationError
from .models import Contato
from .forms import UserRegisterForm
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Contato
from django.contrib.auth.models import User


# REALIZANDO UM NOVO REGISTRO DE USUARIO NO SISTEMA

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.user)

        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email ja existe')
            form = UserRegisterForm(request.POST, request.user)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Sua conta foi criada! Agora você pode se logar {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'tmpl_accounts/register.html', {'form': form})


# CRIANDO UM NOVO CONTATO
class CriandoContato(LoginRequiredMixin, CreateView):
    model = Contato
    fields = ['nome', 'sobrenome', 'telefone', 'email', 'descricao', 'categoria', 'mostrar', 'foto']
    template_name = 'tmpl_accounts/criar_contato.html'

    # SALVANDO E REDIRECIONANDO PARA VER O CONTATO CRIADO
    def form_valid(self, form):

        # FAZENDO RELAÇÃO DO USUARIO LOGADO COM O NOVO CONTATO
        form.instance.criador = self.request.user

        if not form.is_valid():
            messages.error('Erro ao enviar o formulário.')
            return render(self.request, 'tmpl_accounts/criar_contato.html', {'form': form})

        nome = self.request.POST.get('nome')
        email = self.request.POST.get('email')
        telefone = self.request.POST.get('telefone')

        # ------------ VALIDAÇOES DE NOVOS CONTATOS ------------

        # Validando campos vazios
        if not nome or not email or not telefone:
            messages.info(self.request, 'Nenhum campo pode estar vazio.')
            return render(self.request, 'tmpl_accounts/criar_contato.html', {'form': form})

        # Validando campos telefone
        if len(telefone) != 11:
            messages.error(self.request, 'Precisa ter 11 numeros')
            return render(self.request, 'tmpl_accounts/criar_contato.html', {'form': form})

        # Validando email
        try:
            validate_email(email)
            # Vertificando a existencia do mesmo email
            if Contato.objects.filter(email=email).exists():
                messages.error(self.request, 'Email ja existe')
                return render(self.request, 'tmpl_accounts/criar_contato.html', {'form': form})
        except ValidationError:
            messages.error(self.request, 'Email incorreto')
            return render(self.request, 'tmpl_accounts/criar_contato.html', {'form': form})

        # Vertificando a existencia do mesmo telefone
        if Contato.objects.filter(telefone=telefone).exists():
            messages.error(self.request, 'Telefone ja existe')
            return render(self.request, 'tmpl_accounts/criar_contato.html', {'form': form})

        messages.success(self.request, f'Contato {self.request.POST.get("nome")} salvo com sucesso!')
        form.save()
        return super().form_valid(form)
