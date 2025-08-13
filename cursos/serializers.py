
from rest_framework import serializers
from .models import Curso, Leccion, Ejercicio, Progreso, Categoria, ExamenFinal, PreguntaExamenFinal
# Serializador para preguntas del examen final
class PreguntaExamenFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaExamenFinal
        fields = ['id', 'pregunta', 'opciones', 'respuesta_correcta']

# Serializador para el examen final

# Ya no se usa el related_name 'preguntas' en ExamenFinal, sino en Curso
class ExamenFinalSerializer(serializers.ModelSerializer):
    preguntas = serializers.SerializerMethodField()
    curso_titulo = serializers.CharField(source='curso.titulo', read_only=True)

    class Meta:
        model = ExamenFinal
        fields = ['id', 'curso', 'curso_titulo', 'titulo', 'contenido', 'preguntas']

    def get_preguntas(self, obj):
        curso = obj.curso
        preguntas = curso.preguntas_examen_final.all()
        return PreguntaExamenFinalSerializer(preguntas, many=True).data

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class CursoSerializer(serializers.ModelSerializer):
    lecciones_count = serializers.IntegerField(source='lecciones.count', read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'descripcion', 'lecciones_count', 'categoria']

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = ['id', 'pregunta', 'opciones', 'respuesta_correcta']

class LeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leccion
        fields = ['id', 'titulo', 'contenido', 'video_url']

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
            'ejercicios'
        ]

class CursoDetailSerializer(serializers.ModelSerializer):
    lecciones = LeccionSerializer(many=True, read_only=True)
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'descripcion', 'lecciones', 'categoria']

class ProgresoLeccionSerializer(serializers.ModelSerializer):
    leccion_titulo = serializers.CharField(source='leccion.titulo', read_only=True)
    video_url = serializers.CharField(source='leccion.video_url', read_only=True)

    class Meta:
        model = Progreso
        fields = ['leccion', 'leccion_titulo', 'video_url', 'completado', 'puntaje']

class ProgresoCursoSerializer(serializers.Serializer):
    curso_id = serializers.IntegerField()
    curso_titulo = serializers.CharField()
    xp_total = serializers.FloatField()
    porcentaje = serializers.FloatField()
    lecciones = ProgresoLeccionSerializer(many=True)
