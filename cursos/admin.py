from django.contrib import admin
from .models import Curso, Leccion, Ejercicio, Progreso, Inscripcion

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion')

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso')

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'leccion')

@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'leccion', 'completado')

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'fecha_inscripcion')
