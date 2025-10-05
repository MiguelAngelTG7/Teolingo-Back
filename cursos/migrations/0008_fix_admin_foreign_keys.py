from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0007_fix_foreign_keys'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Fix django_admin_log foreign key constraint
            DO $$
            BEGIN
                -- Drop old constraint if it exists
                BEGIN
                    ALTER TABLE django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
                EXCEPTION
                    WHEN others THEN NULL;
                END;
                
                -- Add correct constraint
                BEGIN
                    ALTER TABLE django_admin_log 
                    ADD CONSTRAINT django_admin_log_user_id_fk_usuarios 
                    FOREIGN KEY (user_id) REFERENCES usuarios_usuario(id) DEFERRABLE INITIALLY DEFERRED;
                EXCEPTION
                    WHEN duplicate_object THEN NULL;
                    WHEN others THEN NULL;
                END;
                
                -- También arreglar otras tablas del admin que puedan tener el mismo problema
                BEGIN
                    ALTER TABLE auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
                EXCEPTION
                    WHEN others THEN NULL;
                END;
                
                BEGIN
                    ALTER TABLE auth_permission 
                    ADD CONSTRAINT auth_permission_content_type_id_fk 
                    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
                EXCEPTION
                    WHEN duplicate_object THEN NULL;
                    WHEN others THEN NULL;
                END;
                
            END $$;
            """,
            reverse_sql="-- No reverse needed"
        ),
    ]