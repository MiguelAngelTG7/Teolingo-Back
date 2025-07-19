from django.apps import AppConfig

class CursosConfig(AppConfig):
    name = 'cursos'

    def ready(self):
        import cursos.signals
