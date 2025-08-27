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

@receiver(post_save, sender=Progreso)
def actualizar_progreso_curso(sender, instance, created, **kwargs):
    inscripcion = Inscripcion.objects.get(
        usuario=instance.usuario,
        curso=instance.leccion.curso
    )
    
    total_lecciones = instance.leccion.curso.lecciones.count()
    lecciones_completadas = Progreso.objects.filter(
        usuario=instance.usuario,
        leccion__curso=instance.leccion.curso,
        completado=True
    ).count()
    
    inscripcion.progreso = (lecciones_completadas / total_lecciones) * 100
    inscripcion.save()
