from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, models
from .models import Curso, Leccion, Ejercicio, ExamenFinal, Progreso, Inscripcion
from .serializers import (
    CursoSerializer, 
    LeccionSerializer, 
    EjercicioSerializer,
    ExamenFinalSerializer,
    ProgresoSerializer,
    InscripcionSerializer
)
from datetime import datetime

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CursosListView(APIView):
    def get(self, request):
        try:
            cursos = Curso.objects.all()
            
            # Optimizar consultas
            cursos = cursos.select_related('categoria')
            cursos = cursos.prefetch_related(
                'lecciones',
                'lecciones__ejercicios',
                models.Prefetch(
                    'inscripcion_set',
                    queryset=Inscripcion.objects.filter(usuario=request.user),
                    to_attr='user_inscripcion'
                )
            )
            
            serializer = CursoSerializer(
                cursos, 
                many=True, 
                context={'request': request}
            )
            return Response(serializer.data)
            
        except Exception as e:
            import traceback
            print("Error en CursosListView:", str(e))
            print(traceback.format_exc())
            return Response(
                {'error': 'Error al cargar los cursos'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CursosInscritosView(APIView):
    def get(self, request):
        inscripciones = Inscripcion.objects.filter(usuario=request.user)
        cursos = Curso.objects.filter(inscripcion__in=inscripciones)
        serializer = CursoSerializer(cursos, many=True, context={'request': request})
        return Response(serializer.data)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CursoDetailView(APIView):
    def get(self, request, curso_id):
        curso = get_object_or_404(Curso, id=curso_id)
        serializer = CursoSerializer(curso, context={'request': request})
        return Response(serializer.data)
        
    def post(self, request, curso_id):
        try:
            curso = get_object_or_404(Curso, id=curso_id)
            
            # Verificar si ya está inscrito
            inscripcion_existente = Inscripcion.objects.filter(
                usuario=request.user,
                curso=curso
            ).first()
            
            if inscripcion_existente:
                return Response({
                    'message': 'Ya estás inscrito en este curso'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear nueva inscripción
            inscripcion = Inscripcion.objects.create(
                usuario=request.user,
                curso=curso
            )
            
            serializer = InscripcionSerializer(inscripcion, context={'request': request})
            return Response({
                'message': 'Te has inscrito exitosamente al curso',
                'inscripcion': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Curso.DoesNotExist:
            return Response({
                'error': 'El curso no existe'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class LeccionDetailView(APIView):
    def get(self, request, leccion_id):
        leccion = get_object_or_404(Leccion, id=leccion_id)
        serializer = LeccionSerializer(leccion, context={'request': request})
        return Response(serializer.data)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CursoProgresoView(APIView):
    def get(self, request, curso_id):
        progreso = Progreso.objects.filter(
            usuario=request.user,
            leccion__curso_id=curso_id
        )
        serializer = ProgresoSerializer(progreso, many=True)
        return Response(serializer.data)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class RegistrarRespuestaView(APIView):
    def post(self, request, ejercicio_id):
        ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
        respuesta_usuario = request.data.get('respuesta')
        
        es_correcta = ejercicio.respuesta_correcta == respuesta_usuario
        
        if es_correcta:
            progreso, created = Progreso.objects.get_or_create(
                usuario=request.user,
                leccion=ejercicio.leccion,
                defaults={'completado': True}
            )
        
        return Response({
            'es_correcta': es_correcta,
            'explicacion': ejercicio.explicacion if not es_correcta else None
        })

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ExamenFinalCursoView(APIView):
    def get(self, request, curso_id):
        curso = get_object_or_404(Curso, id=curso_id)
        examen = get_object_or_404(ExamenFinal, curso=curso)
        serializer = ExamenFinalSerializer(examen)
        return Response(serializer.data)

    def post(self, request, curso_id):
        curso = get_object_or_404(Curso, id=curso_id)
        examen = get_object_or_404(ExamenFinal, curso=curso)
        
        # Verificar progreso
        lecciones_completadas = Progreso.objects.filter(
            usuario=request.user,
            leccion__curso=curso,
            completado=True
        ).count()
        
        if lecciones_completadas < curso.lecciones.count():
            return Response({
                'error': 'Debes completar todas las lecciones antes de realizar el examen final'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Procesar respuestas
        respuestas = request.data.get('respuestas', [])
        correctas = 0
        
        for respuesta in respuestas:
            pregunta_id = respuesta.get('pregunta_id')
            respuesta_usuario = respuesta.get('respuesta')
            pregunta = examen.preguntas.get(id=pregunta_id)
            
            if pregunta.respuesta_correcta == respuesta_usuario:
                correctas += 1
        
        total_preguntas = len(examen.preguntas.all())
        porcentaje = (correctas / total_preguntas) * 100
        
        return Response({
            'correctas': correctas,
            'total': total_preguntas,
            'porcentaje': porcentaje,
            'aprobado': porcentaje >= 70
        })

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ActualizarProgresoLeccionView(APIView):
    def post(self, request, leccion_id):
        leccion = get_object_or_404(Leccion, id=leccion_id)
        puntaje = request.data.get('puntaje', 0)
        
        # Crear o actualizar el progreso
        progreso, created = Progreso.objects.update_or_create(
            usuario=request.user,
            leccion=leccion,
            defaults={
                'puntaje': puntaje,
                'completado': True,
                'fecha_completado': datetime.now()
            }
        )
        
        serializer = ProgresoSerializer(progreso)
        return Response({
            'message': 'Progreso actualizado exitosamente',
            'progreso': serializer.data
        })
