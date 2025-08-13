from django.contrib import admin
from django import forms
from .models import Curso, Leccion, Ejercicio, Progreso, Inscripcion, Categoria, ExamenFinal, PreguntaExamenFinal
# Examen Final

from django.utils.html import format_html

@admin.register(ExamenFinal)
class ExamenFinalAdmin(admin.ModelAdmin):
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
        # Mostrar opciones como texto separado por líneas
        if self.instance and self.instance.opciones:
            self.fields['opciones_text'].initial = "\n".join(self.instance.opciones)
            opciones = [(op, op) for op in self.instance.opciones]
        else:
            opciones = []
        # Ocultar el campo original de opciones solo si existe
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
class PreguntaExamenFinalAdmin(admin.ModelAdmin):
    form = PreguntaExamenFinalAdminForm
    list_display = ('id', 'curso', 'pregunta')
    class Media:
        js = ('cursos/admin_ejercicio.js',)

    def curso_editable(self, obj):
        return format_html('<a href="/admin/cursos/curso/{}/change/">{}</a>', obj.curso.id, obj.curso.titulo)
    curso_editable.short_description = 'Curso'
    curso_editable.admin_order_field = 'curso__titulo'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')



# Formulario personalizado para Ejercicio
class EjercicioAdminForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Guardar las opciones como lista
        instance.opciones = self.cleaned_data['opciones_text'] if isinstance(self.cleaned_data['opciones_text'], list) else [self.cleaned_data['opciones_text']]
        # Guardar la respuesta correcta como string
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
        model = Ejercicio
        fields = ['leccion', 'pregunta', 'opciones_text', 'respuesta_correcta']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar opciones como texto separado por líneas
        if self.instance and self.instance.opciones:
            self.fields['opciones_text'].initial = "\n".join(self.instance.opciones)
            opciones = [(op, op) for op in self.instance.opciones]
        else:
            opciones = []
        # Ocultar el campo original de opciones solo si existe
        if 'opciones' in self.fields:
            self.fields['opciones'].widget = forms.HiddenInput()
        # No setear choices para respuesta_correcta, el widget se actualizará solo por JS
        # Setear valor inicial para respuesta_correcta
        if self.instance and self.instance.respuesta_correcta is not None:
            self.fields['respuesta_correcta'].initial = self.instance.respuesta_correcta

    def clean_opciones_text(self):
        data = self.cleaned_data['opciones_text']
        if isinstance(data, list):
            # Ya está procesado
            return data
        return [line.strip() for line in data.splitlines() if line.strip()]

    def clean(self):
        cleaned_data = super().clean()
        opciones = self.clean_opciones_text()
        cleaned_data['opciones'] = opciones
        # Si la respuesta correcta no está entre las opciones, la borra
        if cleaned_data.get('respuesta_correcta') not in opciones:
            cleaned_data['respuesta_correcta'] = ''
        return cleaned_data

from django.utils.html import format_html

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo_editable', 'categoria')
    list_filter = ('categoria',)

    def titulo_editable(self, obj):
        return format_html('<a href="/admin/cursos/curso/{}/change/">{}</a>', obj.id, obj.titulo)
    titulo_editable.short_description = 'Título'
    titulo_editable.admin_order_field = 'titulo'

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    pass

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    form = EjercicioAdminForm
    list_display = ('pregunta', 'leccion')
    class Media:
        js = ('cursos/admin_ejercicio.js',)

@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    pass

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    pass
