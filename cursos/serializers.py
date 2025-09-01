from rest_framework import serializers
from .models import Categoria, Curso, Leccion, Ejercicio, ExamenFinal, PreguntaExamenFinal, Progreso, Inscripcion

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = ('id', 'pregunta', 'opciones', 'respuesta_correcta', 'explicacion')

class LeccionSerializer(serializers.ModelSerializer):
    ejercicios = EjercicioSerializer(many=True, read_only=True)
    completada = serializers.SerializerMethodField()

    class Meta:
        model = Leccion
        fields = ('id', 'titulo', 'contenido', 'ejercicios', 'completada')

    def get_completada(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Progreso.objects.filter(
                usuario=request.user,
                leccion=obj,
                completado=True
            ).exists()
        return False

class CursoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    lecciones = LeccionSerializer(many=True, read_only=True)
    progreso_total = serializers.SerializerMethodField()
    esta_inscrito = serializers.SerializerMethodField()
    
    class Meta:
        model = Curso
        fields = ('id', 'titulo', 'descripcion', 'categoria', 'lecciones', 'progreso_total', 'esta_inscrito')
        
    def get_esta_inscrito(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            try:
                return Inscripcion.objects.filter(
                    usuario=request.user,
                    curso=obj
                ).exists()
            except Exception:
                return False
        return False

    def get_progreso_total(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            total_lecciones = obj.lecciones.count()
            if total_lecciones == 0:
                return 0
            
            lecciones_completadas = Progreso.objects.filter(
                usuario=request.user,
                leccion__curso=obj,
                completado=True
            ).count()
            
            return int((lecciones_completadas / total_lecciones) * 100)
        return 0

class PreguntaExamenFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaExamenFinal
        fields = ('id', 'pregunta', 'opciones', 'respuesta_correcta')

class ExamenFinalSerializer(serializers.ModelSerializer):
    preguntas = serializers.SerializerMethodField()
    curso_titulo = serializers.CharField(source='curso.titulo', read_only=True)
    curso_id = serializers.IntegerField(source='curso.id', read_only=True)
    
    class Meta:
        model = ExamenFinal
        fields = ('id', 'titulo', 'contenido', 'preguntas', 'curso_titulo', 'curso_id')
    
    def get_preguntas(self, obj):
        preguntas = []
        # Usamos order_by('id') para ordenar por ID de forma ascendente
        for pregunta in PreguntaExamenFinal.objects.filter(curso=obj.curso).order_by('id'):
            preguntas.append({
                'id': pregunta.id,
                'pregunta': pregunta.pregunta,
                'opciones': pregunta.opciones,
                'respuesta_correcta': pregunta.respuesta_correcta
            })
        return preguntas

class ProgresoSerializer(serializers.ModelSerializer):
    leccion_titulo = serializers.CharField(source='leccion.titulo', read_only=True)
    
    class Meta:
        model = Progreso
        fields = ('id', 'leccion', 'leccion_titulo', 'completado')

class InscripcionSerializer(serializers.ModelSerializer):
    curso_titulo = serializers.CharField(source='curso.titulo', read_only=True)
    progreso_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Inscripcion
        fields = ('id', 'curso', 'curso_titulo', 'fecha_inscripcion', 'completado', 'progreso_total')
        read_only_fields = ('fecha_inscripcion', 'completado', 'progreso_total')
        
    def get_progreso_total(self, obj):
        total_lecciones = obj.curso.lecciones.count()
        if total_lecciones == 0:
            return 0
        
        lecciones_completadas = Progreso.objects.filter(
            usuario=obj.usuario,
            leccion__curso=obj.curso,
            completado=True
        ).count()
        
        return int((lecciones_completadas / total_lecciones) * 100) if total_lecciones > 0 else 0
