from django.contrib import admin
from django import forms
from import_export.admin import ImportExportModelAdmin
from .models import Curso, Leccion, Ejercicio, Progreso, Inscripcion, Categoria, ExamenFinal, PreguntaExamenFinal
# Examen Final

from django.utils.html import format_html

@admin.register(ExamenFinal)
class ExamenFinalAdmin(ImportExportModelAdmin):
    list_display = ('id', 'curso', 'titulo')

    def curso_editable(self, obj):
        return format_html('<a href="/admin/cursos/curso/{}/change/">{}</a>', obj.curso.id, obj.curso.titulo)
    curso_editable.short_description = 'Curso'
    curso_editable.admin_order_field = 'curso__titulo'

# Formulario personalizado para PreguntaExamenFinal
class PreguntaExamenFinalAdminForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.opciones = self.cleaned_data['opciones_text'] if isinstance(self.cleaned_data['opciones_text'], list) else [self.cleaned_data['opciones_text']]
        instance.respuesta_correcta = self.cleaned_data.get('respuesta_correcta', '')
        if commit:
            instance.save()
        return instance
    opciones_text = forms.CharField(
        label="Opciones (una por línea)",
        widget=forms.Textarea,
        required=False,
        help_text="Escribe una opción por línea."
    )

    respuesta_correcta = forms.CharField(
        label="Respuesta correcta",
        required=False,
        help_text="Selecciona la respuesta correcta.",
        widget=forms.Select(choices=[])
    )

    class Meta:
        model = PreguntaExamenFinal
        fields = ['curso', 'pregunta', 'opciones_text', 'respuesta_correcta']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.opciones:
            self.fields['opciones_text'].initial = "\n".join(self.instance.opciones)
            opciones = [(op, op) for op in self.instance.opciones]
        else:
            opciones = []
        if 'opciones' in self.fields:
            self.fields['opciones'].widget = forms.HiddenInput()
        self.fields['respuesta_correcta'].widget.choices = opciones
        if self.instance and self.instance.respuesta_correcta is not None:
            self.fields['respuesta_correcta'].initial = self.instance.respuesta_correcta

    def clean_opciones_text(self):
        data = self.cleaned_data['opciones_text']
        if isinstance(data, list):
            return data
        return [line.strip() for line in data.splitlines() if line.strip()]

    def clean(self):
        cleaned_data = super().clean()
        opciones = self.clean_opciones_text()
        cleaned_data['opciones'] = opciones
        if cleaned_data.get('respuesta_correcta') not in opciones:
            cleaned_data['respuesta_correcta'] = ''
        return cleaned_data

@admin.register(PreguntaExamenFinal)
class PreguntaExamenFinalAdmin(ImportExportModelAdmin):
    form = PreguntaExamenFinalAdminForm
    list_display = ('id', 'curso', 'pregunta')
    class Media:
        js = ('cursos/admin_ejercicio.js',)

    def curso_editable(self, obj):
        return format_html('<a href="/admin/cursos/curso/{}/change/">{}</a>', obj.curso.id, obj.curso.titulo)
    curso_editable.short_description = 'Curso'
    curso_editable.admin_order_field = 'curso__titulo'

@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nombre')

# Formulario personalizado para Ejercicio
class EjercicioAdminForm(forms.ModelForm):
    opcion = forms.CharField(
        label="Opciones (formato JSON)",
        widget=forms.Textarea,
        required=False,
        help_text="Escribe las opciones en formato JSON: ['Opción 1', 'Opción 2', ...]"
    )

    class Meta:
        model = Ejercicio
        fields = ['leccion', 'pregunta', 'opcion', 'respuesta_correcta']

    def clean_opcion(self):
        import json
        data = self.cleaned_data['opcion']
        try:
            opciones = json.loads(data.replace("'", '"'))
            if not isinstance(opciones, list):
                raise forms.ValidationError("El campo debe ser una lista JSON.")
            return opciones
        except Exception as e:
            raise forms.ValidationError(f"Formato JSON inválido: {e}")

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['opciones'] = cleaned_data.get('opcion', [])
        return cleaned_data

@admin.register(Curso)
class CursoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'titulo_editable', 'categoria')
    list_filter = ('categoria',)

    def titulo_editable(self, obj):
        return format_html('<a href="/admin/cursos/curso/{}/change/">{}</a>', obj.id, obj.titulo)
    titulo_editable.short_description = 'Título'
    titulo_editable.admin_order_field = 'titulo'

@admin.register(Leccion)
class LeccionAdmin(ImportExportModelAdmin):
    pass

@admin.register(Ejercicio)
class EjercicioAdmin(ImportExportModelAdmin):
    form = EjercicioAdminForm
    list_display = ('pregunta', 'leccion')
    class Media:
        js = ('cursos/admin_ejercicio.js',)

@admin.register(Progreso)
class ProgresoAdmin(ImportExportModelAdmin):
    pass

@admin.register(Inscripcion)
class InscripcionAdmin(ImportExportModelAdmin):
    pass
