from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Curso, Leccion, Progreso, ExamenFinal
from .serializers import CursoSerializer, CursoDetailSerializer, LeccionDetailSerializer, ProgresoCursoSerializer, ProgresoLeccionSerializer, ExamenFinalSerializer

# Vista para obtener el examen final de un curso
class ExamenFinalCursoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, curso_id):
        curso = get_object_or_404(Curso, id=curso_id)
        examen = getattr(curso, 'examen_final', None)
        if not examen:
            return Response({'detail': 'Este curso no tiene examen final.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExamenFinalSerializer(examen)
        return Response(serializer.data)

class CursosInscritosView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cursos = Curso.objects.filter(inscripcion__usuario=request.user)
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)

class CursoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        curso = get_object_or_404(Curso, id=id)
        if not curso.esta_inscrito(request.user):
            return Response({"detail": "No estás inscrito en este curso."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CursoDetailSerializer(curso)
        return Response(serializer.data)

class LeccionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        leccion = get_object_or_404(Leccion, id=id)
        if not leccion.curso.esta_inscrito(request.user):
            return Response({"detail": "No estás inscrito en esta lección."}, status=status.HTTP_403_FORBIDDEN)
        serializer = LeccionDetailSerializer(leccion)
        return Response(serializer.data)

class CursoProgresoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        curso = get_object_or_404(Curso, id=id)
        lecciones = curso.lecciones.all()
        progresos = Progreso.objects.filter(usuario=request.user, leccion__in=lecciones)
        lecciones_data = []
        for leccion in lecciones:
            progreso = progresos.filter(leccion=leccion).first()
            lecciones_data.append({
                "leccion": leccion.id,
                "leccion_titulo": leccion.titulo,
                "completado": progreso.completado if progreso else False,
                "puntaje": progreso.puntaje if progreso else 0
            })
        xp_total = sum(p.puntaje for p in progresos)
        completadas = sum(1 for p in progresos if p.completado)
        porcentaje = (completadas / lecciones.count()) * 100 if lecciones.count() > 0 else 0
        data = {
            "curso_id": curso.id,
            "curso_titulo": curso.titulo,
            "xp_total": xp_total,
            "porcentaje": porcentaje,
            "lecciones": lecciones_data
        }
        return Response(data)

class RegistrarRespuestaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        leccion = get_object_or_404(Leccion, id=id)
        puntaje = request.data.get('puntaje', 0)
        progreso, created = Progreso.objects.get_or_create(usuario=request.user, leccion=leccion)
        progreso.puntaje = puntaje
        progreso.completado = True
        progreso.save()
        return Response({"ok": True, "puntaje": progreso.puntaje})

    def get(self, request, id):
        print("Usuario autenticado:", request.user)
        leccion = get_object_or_404(Leccion, id=id)
        if not leccion.curso.esta_inscrito(request.user):
            return Response({"detail": "No estás inscrito en esta lección."}, status=status.HTTP_403_FORBIDDEN)
        serializer = LeccionDetailSerializer(leccion)
        return Response(serializer.data)
