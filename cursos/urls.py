from django.urls import path
from .views import CursosInscritosView, CursoDetailView, LeccionDetailView

urlpatterns = [
    path('cursos/', CursosInscritosView.as_view(), name='cursos_inscritos'),
    path('cursos/<int:id>/', CursoDetailView.as_view(), name='curso_detail'),
    path('lecciones/<int:id>/', LeccionDetailView.as_view(), name='leccion_detail'),
]
