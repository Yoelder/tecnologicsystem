from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class NombreOrCorreoBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        Usuario = get_user_model()  # Obtiene el modelo de usuario personalizado
        try:
            # Intentar autenticar con el nombre
            usuario = Usuario.objects.get(nombre=username)
        except Usuario.DoesNotExist:
            # Si no se encuentra por nombre, intentar con el correo
            try:
                usuario = Usuario.objects.get(correo=username)
            except Usuario.DoesNotExist:
                return None

        # Verificar si la contraseña es correcta
        if usuario.check_password(password):
            return usuario
        return None

    def get_user(self, user_id):
        Usuario = get_user_model()
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
