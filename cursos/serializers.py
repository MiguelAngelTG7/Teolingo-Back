from rest_framework import serializers
from .models import Curso, Leccion, Ejercicio

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'descripcion']

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = ['id', 'pregunta', 'opciones', 'respuesta_correcta']

class LeccionDetailSerializer(serializers.ModelSerializer):
    ejercicios = EjercicioSerializer(many=True, read_only=True)

    class Meta:
        model = Leccion
        fields = ['id', 'titulo', 'contenido', 'ejercicios']

class CursoDetailSerializer(serializers.ModelSerializer):
    lecciones = LeccionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'descripcion', 'lecciones']
