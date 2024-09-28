from .models import Navegacion
from django.utils.deprecation import MiddlewareMixin

class RegistroNavegacionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            Navegacion.objects.create(
                usuario=request.user,
                url=request.path,
                metodo_http=request.method,
                ip=request.META.get('REMOTE_ADDR'),
                agente_usuario=request.META.get('HTTP_USER_AGENT'),
            )
