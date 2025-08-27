from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'nombre_completo', 'is_staff', 'is_active', 'email_verificado')
    list_filter = ('is_staff', 'is_active', 'email_verificado')
    search_fields = ('email', 'nombre_completo')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login', 'token_verificacion', 'token_verificacion_fecha', 
                      'token_reset_password', 'token_reset_password_fecha')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre_completo',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login',)}),
        ('Estado de verificación', {'fields': ('email_verificado', 'token_verificacion', 'token_verificacion_fecha', 'token_reset_password', 'token_reset_password_fecha')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre_completo', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(Usuario, CustomUserAdmin)
