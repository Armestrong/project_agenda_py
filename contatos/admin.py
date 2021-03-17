from django.contrib import admin

# Register your models here.
from .models import Contato


# PREPARANDO OS CAMPOS DO ADMIN
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email', 'data_criacao', 'categoria', 'mostrar', 'foto')
    list_display_links = ('id', 'nome', 'sobrenome')
    # list_filter = ('nome', 'sobrenome')
    list_per_page = 10
    search_fields = ('nome', 'sobrenome')
    list_editable = ('telefone', 'mostrar')


# ENVIANDO OBJETO CONTATO E CONTATOADMIN PARA VIEW
admin.site.register(Contato, ContatoAdmin)
