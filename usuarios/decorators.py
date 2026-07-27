from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """
    Decorador para vistas que asegura que el usuario autenticado sea administrador
    (superuser). Si es un conductor, lo redirige al dashboard con un mensaje de alerta.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # 1. Verificar que esté logueado y sea superusuario
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        # 2. Si es un conductor o usuario común, denegar acceso
        messages.error(request, "No tienes permisos de administrador para acceder a este módulo.")
        return redirect('dashboard')  # Asegúrate de que 'dashboard' sea el nombre de tu URL del home
        
    return _wrapped_view