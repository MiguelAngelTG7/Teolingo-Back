from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo

    def esta_inscrito(self, usuario):
        return self.inscripcion_set.filter(usuario=usuario).exists()

class Leccion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()

    def __str__(self):
        return self.titulo

class Ejercicio(models.Model):
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name='ejercicios')
    pregunta = models.TextField()
    opciones = models.JSONField(default=list)
    respuesta_correcta = models.JSONField(default=list)

    def __str__(self):
        return self.pregunta

class Progreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    puntaje = models.FloatField(default=0)

    class Meta:
        unique_together = ('usuario', 'leccion')

class Inscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'curso')
