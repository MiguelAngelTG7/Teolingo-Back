from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0006_alter_preguntaexamenfinal_options_and_more'),  # Cambiado aquí
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Drop the old foreign key constraint
        migrations.RunSQL(
            "ALTER TABLE cursos_inscripcion DROP CONSTRAINT IF EXISTS cursos_inscripcion_usuario_id_3fd76652_fk_auth_user_id;",
            reverse_sql="-- No reverse"
        ),
        
        # Drop the old foreign key constraint for progreso table too
        migrations.RunSQL(
            "ALTER TABLE cursos_progreso DROP CONSTRAINT IF EXISTS cursos_progreso_usuario_id_d0ed5718_fk_auth_user_id;",
            reverse_sql="-- No reverse"
        ),
        
        # Recreate the field with correct foreign key
        migrations.AlterField(
            model_name='inscripcion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        
        migrations.AlterField(
            model_name='progreso',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progresos', to=settings.AUTH_USER_MODEL),
        ),
    ]