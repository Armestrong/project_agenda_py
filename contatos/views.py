from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


# Create your views here.
def index(request):
    contato = Contato.objects.order_by('-id').filter(
        mostrar=True
    )

    paginator = Paginator(contato, 4)

    page = request.GET.get('p')
    contato = paginator.get_page(page)
    return render(request, 'tmpl_contatos/index.html', {
        'contatos': contato
    })


def ver_contato(request, contato_id):
    # contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostrar:
        raise Http404()

    return render(request, 'tmpl_contatos/ver_contato.html', {
        'contato': contato
    })


def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(request, messages.ERROR, 'Campo termo não pode ficar vazio.'),
        return redirect('index')

    campos = Concat('nome', Value(' '), 'sobrenome')
    contato = Contato.objects.annotate(
        nome_completo=campos

    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )
    # contato = Contato.objects.order_by('-id').filter(
    #     Q(nome__icontains=termo) | Q(sobrenome__icontains=termo),
    #     mostrar=True
    # )

    paginator = Paginator(contato, 4)

    page = request.GET.get('p')
    contato = paginator.get_page(page)
    return render(request, 'tmpl_contatos/busca.html', {
        'contatos': contato
    })
