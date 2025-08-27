from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='cursos', null=True, blank=True)

    def __str__(self):
        return self.titulo

    def esta_inscrito(self, usuario):
        return self.inscripcion_set.filter(usuario=usuario).exists()


class ExamenFinal(models.Model):
    curso = models.OneToOneField(Curso, on_delete=models.CASCADE, related_name='examen_final')
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()

    def __str__(self):
        return f"Examen Final: {self.titulo}"


class PreguntaExamenFinal(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='preguntas_examen_final')
    pregunta = models.TextField()
    opciones = models.JSONField(default=list)
    respuesta_correcta = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']  # Ordenar por ID de forma ascendente

    def __str__(self):
        return self.pregunta


class Inscripcion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['usuario', 'curso']
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'

    def __str__(self):
        return f"{self.usuario.email} - {self.curso.titulo}"

class Leccion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

class Ejercicio(models.Model):
    leccion = models.ForeignKey('Leccion', on_delete=models.CASCADE, related_name='ejercicios')
    pregunta = models.CharField(max_length=500)
    opciones = models.JSONField(default=list)
    respuesta_correcta = models.CharField(max_length=500, default='')
    explicacion = models.TextField(blank=True)
    puntaje = models.IntegerField(
        default=10,  # Valor por defecto explícito
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        help_text="Puntaje del ejercicio (0-100)"
    )

    class Meta:
        verbose_name = 'Ejercicio'
        verbose_name_plural = 'Ejercicios'
        ordering = ['id']

    def __str__(self):
        return f"Ejercicio: {self.pregunta[:50]}..."

    def clean(self):
        if self.puntaje < 0 or self.puntaje > 100:
            raise ValidationError('El puntaje debe estar entre 0 y 100')

class Progreso(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Changed from auth.User
        on_delete=models.CASCADE,
        related_name='progresos'
    )
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    puntaje = models.FloatField(default=0)

    class Meta:
        unique_together = ('usuario', 'leccion')


