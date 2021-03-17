from django.apps import AppConfig


class ContatosConfig(AppConfig):
    name = 'contatos'

    def ready(self):
        import contatos.signals
