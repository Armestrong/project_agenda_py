from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from enum import Enum


# Create your models here.

# CRIANDO UMA CLASSE CONTATO PARA INTERAGIR COM A VIEW E POPULAR O BANCO
# UTILIZANDO A METODOLOGIA ORM
class Contato(models.Model):
    # CRIANDO UMA SUBCLASSE ENUM
    class Categoria(models.TextChoices):
        FAMILIA = "Família"
        AMIGO = "Amigo"
        CONHECIDO = "Conhecido"
        VIZINHO = "Vizinho(a)"

    criador = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=40)
    sobrenome = models.CharField(max_length=40, blank=True)
    telefone = models.CharField(max_length=40)
    email = models.CharField(max_length=40, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=50, choices=Categoria.choices, default=Categoria.CONHECIDO)
    mostrar = models.BooleanField(default=True)
    foto = models.ImageField(default='default.jpg', upload_to='pictures/%Y/%m/%d')

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Resize images
        # img = Image.open(self.foto.path)
        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.foto.path)
        # Padronizando Strings
        self.nome = self.nome.title()
        self.sobrenome = self.sobrenome.title()
        super(Contato, self).save(*args, **kwargs)

    # PASSANDO A PK PARA VIEW
    def get_absolute_url(self):
        return reverse('ver_contato', kwargs={'contato_id': self.pk})
