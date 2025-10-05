from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0006_alter_preguntaexamenfinal_options_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Fix foreign key constraints to point to custom user model
            DO $$
            BEGIN
                -- Drop old constraints if they exist
                EXECUTE 'ALTER TABLE cursos_inscripcion DROP CONSTRAINT IF EXISTS cursos_inscripcion_usuario_id_3fd76652_fk_auth_user_id';
                EXECUTE 'ALTER TABLE cursos_progreso DROP CONSTRAINT IF EXISTS cursos_progreso_usuario_id_d0ed5718_fk_auth_user_id';
                
                -- Add correct constraints
                EXECUTE 'ALTER TABLE cursos_inscripcion ADD CONSTRAINT cursos_inscripcion_usuario_id_fk_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios_usuario(id) DEFERRABLE INITIALLY DEFERRED';
                EXECUTE 'ALTER TABLE cursos_progreso ADD CONSTRAINT cursos_progreso_usuario_id_fk_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios_usuario(id) DEFERRABLE INITIALLY DEFERRED';
            EXCEPTION
                WHEN others THEN
                    -- Ignore errors if constraints already exist or other issues
                    NULL;
            END $$;
            """,
            reverse_sql="-- No reverse needed"
        ),
    ]