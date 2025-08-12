from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("cursos", "0008_curso_imagen_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="curso",
            name="imagen_url",
        ),
        migrations.RemoveField(
            model_name="leccion",
            name="guia_pdf_url",
        ),
    ]
