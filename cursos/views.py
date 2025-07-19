from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Curso, Leccion
from .serializers import CursoSerializer, CursoDetailSerializer, LeccionDetailSerializer

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
