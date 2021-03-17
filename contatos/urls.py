from django.urls import path
from .views import Index, MeusContatos, ver_contato, busca

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('busca/', busca, name='busca'),
    path('<int:contato_id>', ver_contato, name='ver_contato'),
    path('usuario/<str:username>', MeusContatos.as_view(), name='usuario-contato'),
]
