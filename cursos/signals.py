from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inscripcion, Leccion, Progreso

@receiver(post_save, sender=Inscripcion)
def crear_progreso_lecciones(sender, instance, created, **kwargs):
    if created:
        lecciones = Leccion.objects.filter(curso=instance.curso)
        for leccion in lecciones:
            Progreso.objects.get_or_create(
                usuario=instance.usuario,
                leccion=leccion,
                defaults={'completado': False, 'puntaje': 0}
            )
