from django.db import models
from contatos.models import Contato
from django import forms


# PEGANGO O MODELS CRIADO EM CONTATOS E UTILIZANDO EM ACCOUNTS
class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        exclude = ()
