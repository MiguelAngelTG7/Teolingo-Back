from django.contrib import admin
from django import forms
from .models import Curso, Leccion, Ejercicio, Progreso, Inscripcion

# Formulario personalizado para Ejercicio
class EjercicioAdminForm(forms.ModelForm):
    opciones_text = forms.CharField(
        label="Opciones (una por línea)",
        widget=forms.Textarea,
        required=False,
        help_text="Escribe una opción por línea."
    )

    respuesta_correcta = forms.ChoiceField(
        label="Respuesta correcta",
        choices=[],
        required=False,
        help_text="Selecciona la respuesta correcta."
    )

    class Meta:
        model = Ejercicio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar opciones como texto separado por líneas
        if self.instance and self.instance.opciones:
            self.fields['opciones_text'].initial = "\n".join(self.instance.opciones)
            opciones = [(op, op) for op in self.instance.opciones]
        else:
            opciones = []
        # Ocultar el campo original de opciones
        self.fields['opciones'].widget = forms.HiddenInput()
        # Setear choices para respuesta_correcta
        self.fields['respuesta_correcta'].choices = opciones
        # Setear valor inicial para respuesta_correcta
        if self.instance and self.instance.respuesta_correcta:
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

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    pass

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    pass

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    form = EjercicioAdminForm
    list_display = ('pregunta', 'leccion')

@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    pass

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    pass
