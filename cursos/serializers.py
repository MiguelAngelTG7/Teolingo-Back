from rest_framework import serializers
from .models import Curso, Leccion, Ejercicio, Progreso

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'descripcion']

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = ['id', 'pregunta', 'opciones', 'respuesta_correcta']

class LeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leccion
        fields = ['id', 'titulo', 'contenido', 'video_url', 'guia_pdf_url']

class LeccionDetailSerializer(serializers.ModelSerializer):
    curso_id = serializers.IntegerField(source='curso.id', read_only=True)
    ejercicios = EjercicioSerializer(many=True, read_only=True)

    class Meta:
        model = Leccion
        fields = [
            'id',
            'curso_id',
            'titulo',
            'contenido',
            'video_url',
            'guia_pdf_url',
            'ejercicios'
        ]

class CursoDetailSerializer(serializers.ModelSerializer):
    lecciones = LeccionSerializer(many=True, read_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'descripcion', 'lecciones']

class ProgresoLeccionSerializer(serializers.ModelSerializer):
    leccion_titulo = serializers.CharField(source='leccion.titulo', read_only=True)
    video_url = serializers.CharField(source='leccion.video_url', read_only=True)
    guia_pdf_url = serializers.CharField(source='leccion.guia_pdf_url', read_only=True)

    class Meta:
        model = Progreso
        fields = ['leccion', 'leccion_titulo', 'video_url', 'guia_pdf_url', 'completado', 'puntaje']

class ProgresoCursoSerializer(serializers.Serializer):
    curso_id = serializers.IntegerField()
    curso_titulo = serializers.CharField()
    xp_total = serializers.FloatField()
    porcentaje = serializers.FloatField()
    lecciones = ProgresoLeccionSerializer(many=True)
