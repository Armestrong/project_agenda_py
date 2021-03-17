from django.shortcuts import render, get_object_or_404
from .models import Contato
from django.http import Http404

from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.models import User


# PAGINA PRINCIPAL
class Index(ListView):
    model = Contato
    template_name = 'tmpl_contatos/index.html'
    # put the content on the view/page
    context_object_name = 'contatos'
    paginate_by = 5


# VISUALIZAR AS INSFORMAÇOES DO CONTATO
def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if not contato.mostrar:
        raise Http404()
    return render(request, 'tmpl_contatos/ver_contato.html', {
        'contato': contato
    })


# BUSCAR CONTATO POR NOME E/OU SOBRENOME
def busca(request):
    user = request.user.is_authenticated
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(request, messages.ERROR, 'Campo busca não pode ficar vazio.'),

    campos = Concat('nome', Value(' '), 'sobrenome')
    contato = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo), criador=user
    )

    return render(request, 'tmpl_contatos/meus_contatos.html', {
        'posts': contato
    })


# VER TODOS OS CONTATOS QUE EU CRIEI
class MeusContatos(ListView):
    model = Contato
    template_name = 'tmpl_contatos/meus_contatos.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Contato.objects.filter(criador=user).order_by('-data_criacao')
