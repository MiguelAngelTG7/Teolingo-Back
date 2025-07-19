import json
from cursos.models import Curso, Leccion, Ejercicio

def cargar_curso_desde_json(archivo_path):
    with open(archivo_path, encoding='utf-8') as f:
        data = json.load(f)

    curso_data = data["curso"]
    curso = Curso.objects.create(
        titulo=curso_data["titulo"],
        descripcion=curso_data["descripcion"],
        nivel=curso_data["nivel"]
    )

    for leccion_data in curso_data["lecciones"]:
        leccion = Leccion.objects.create(
            curso=curso,
            orden=leccion_data["orden"],
            titulo=leccion_data["titulo"],
            introduccion=leccion_data["introduccion"],
            resumen=leccion_data["resumen"]
        )

        for ejercicio_data in leccion_data["ejercicios"]:
            Ejercicio.objects.create(
                leccion=leccion,
                tipo=ejercicio_data["tipo"],
                pregunta=ejercicio_data.get("pregunta", ""),
                versiculo=ejercicio_data.get("versiculo", ""),
                opciones=ejercicio_data.get("opciones"),
                respuesta_correcta=ejercicio_data["respuesta_correcta"]
            )

    print("✅ Curso cargado exitosamente.")
        