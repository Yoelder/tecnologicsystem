# usuarios/admin.py

from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'tipo_usuario', 'is_active')
    search_fields = ('nombre', 'correo', 'tipo_usuario')

# usuarios/admin.py




