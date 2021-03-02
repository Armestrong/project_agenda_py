from django.db import models
from django.utils import timezone


# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=40)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=40)
    sobrenome = models.CharField(max_length=40, blank=True)
    telefone = models.CharField(max_length=40)
    email = models.CharField(max_length=40, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)
    foto = models.ImageField(blank=True, upload_to='pictures/%Y/%m/%d')

    def __str__(self):
        return self.nome
