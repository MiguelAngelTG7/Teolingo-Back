from django.urls import path
from .views import (
    CursosListView,
    CursosInscritosView,
    CursoDetailView,
    LeccionDetailView,
    CursoProgresoView,
    RegistrarRespuestaView,
    ExamenFinalCursoView,
    ActualizarProgresoLeccionView
)

urlpatterns = [
    path('', CursosListView.as_view(), name='cursos-list'),
    path('inscritos/', CursosInscritosView.as_view(), name='cursos-inscritos'),
    path('<int:curso_id>/', CursoDetailView.as_view(), name='curso-detail'),
    path('leccion/<int:leccion_id>/', LeccionDetailView.as_view(), name='leccion-detail'),
    path('<int:curso_id>/progreso/', CursoProgresoView.as_view(), name='curso-progreso'),
    path('ejercicio/<int:ejercicio_id>/respuesta/', RegistrarRespuestaView.as_view(), name='registrar-respuesta'),
    path('<int:curso_id>/examen-final/', ExamenFinalCursoView.as_view(), name='examen-final'),
    path('leccion/<int:leccion_id>/progreso/', ActualizarProgresoLeccionView.as_view(), name='actualizar-progreso-leccion'),
]
