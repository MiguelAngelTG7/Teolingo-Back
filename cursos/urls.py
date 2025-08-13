from django.urls import path
from .views import CursosInscritosView, CursoDetailView, LeccionDetailView, CursoProgresoView, RegistrarRespuestaView, ExamenFinalCursoView

urlpatterns = [
    path('cursos/', CursosInscritosView.as_view(), name='cursos_inscritos'),
    path('cursos/<int:id>/', CursoDetailView.as_view(), name='curso_detail'),
    path('cursos/<int:id>/progreso/', CursoProgresoView.as_view(), name='curso_progreso'),
    path('cursos/<int:curso_id>/examen-final/', ExamenFinalCursoView.as_view(), name='examen_final_curso'),
    path('lecciones/<int:id>/', LeccionDetailView.as_view(), name='leccion_detail'),
    path('lecciones/<int:id>/respuesta/', RegistrarRespuestaView.as_view(), name='registrar_respuesta'),
]
