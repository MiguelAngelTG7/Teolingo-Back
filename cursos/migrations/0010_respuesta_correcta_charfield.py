from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("cursos", "0009_remove_imagenurl_guiapdfurl"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ejercicio",
            name="respuesta_correcta",
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
    ]
