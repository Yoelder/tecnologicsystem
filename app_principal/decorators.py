from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

from django.contrib import messages

from django.shortcuts import redirect

def profesor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.tipo_usuario == 'profesor' or request.user.tipo_usuario == 'admin'):
            return view_func(request, *args, **kwargs)
        else:
            # Envía el mensaje de error
            messages.error(request, "No tienes los privilegios suficientes para acceder a esta página.")
            # Redirige siempre a la página 'home'
            return redirect('/home/')
    return _wrapped_view
