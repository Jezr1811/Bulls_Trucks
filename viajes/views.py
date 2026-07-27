from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from usuarios.decorators import admin_required
from .forms import ViajeForm
from .models import Viaje

# =========================================================================
# 1. VISTAS DE LECTURA (READ)
# =========================================================================

@login_required
def lista_viajes(request):
    """
    Muestra el listado de viajes aplicando filtros de seguridad según el rol:
    - Superusuario: Ve todos los viajes.
    - Conductor: Solo ve los viajes que tiene asignados.
    - Otros/Sin rol: No ven ningún viaje.
    """
    if request.user.is_superuser:
        viajes = Viaje.objects.all().order_by("-id")
    elif hasattr(request.user, 'conductor'):
        viajes = Viaje.objects.filter(conductor=request.user.conductor).order_by("-id")
    else:
        viajes = Viaje.objects.none()

    return render(
        request,
        "viajes/lista.html",
        {"viajes": viajes},
    )


@login_required
def detalle_viaje(request, pk):
    """
    Muestra el menú interno y detalles específicos de un viaje activo.
    Aplica capa de seguridad para evitar que conductores vean viajes ajenos.
    """
    if request.user.is_superuser:
        viaje = get_object_or_404(Viaje, pk=pk)
    else:
        viaje = get_object_or_404(Viaje, pk=pk, conductor=request.user.conductor)

    return render(
        request,
        "viajes/detalle.html",
        {"viaje": viaje}
    )


# =========================================================================
# 2. GESTIÓN DE ESTADOS (STATE MANAGEMENT)
# =========================================================================

@login_required
def cambiar_estado_viaje(request, pk, accion):
    """
    Controla el flujo de estados del viaje (pendiente -> en_curso -> finalizado).
    Registra automáticamente las marcas de tiempo correspondientes.
    """
    if request.user.is_superuser:
        viaje = get_object_or_404(Viaje, pk=pk)
    else:
        viaje = get_object_or_404(Viaje, pk=pk, conductor=request.user.conductor)
    
    # Transición: De 'Pendiente' a 'En Curso'
    if accion == "iniciar" and viaje.estado == "pendiente":
        viaje.estado = "en_curso"
        viaje.fecha_inicio = timezone.now().date()
        messages.success(request, "¡Buen viaje! La ruta ha pasado a estar 'En Curso'.")
        
    # Transición: De 'En Curso' a 'Finalizado'
    elif accion == "terminar" and viaje.estado == "en_curso":
        viaje.estado = "finalizado"
        # Descomenta la siguiente línea si agregas 'fecha_fin' a tu base de datos:
        # viaje.fecha_fin = timezone.now().date()  
        messages.success(request, "Operación concluida. Viaje finalizado correctamente.")
        
    viaje.save()
    return redirect("viajes:detalle_viaje", pk=viaje.id)


# =========================================================================
# 3. OPERACIONES DE ESCRITURA (CRUD)
# =========================================================================

@login_required
def crear_viaje(request):
    """
    Registra un nuevo viaje en el sistema. Si el usuario actual es un conductor,
    lo asigna automáticamente como el responsable del viaje.
    """
    if request.method == "POST":
        form = ViajeForm(request.POST, user=request.user)
        if form.is_valid():
            viaje = form.save(commit=False)
            if not request.user.is_superuser:
                viaje.conductor = request.user.conductor
            viaje.save()
            messages.success(request, "Viaje registrado con éxito.")
            return redirect("viajes:lista_viajes")
    else:
        form = ViajeForm(user=request.user)

    return render(request, "viajes/formulario.html", {"form": form})


@login_required
def editar_viaje(request, pk):
    """
    Permite la edición de los datos de un viaje existente previa validación 
    de permisos del usuario solicitante.
    """
    if request.user.is_superuser:
        viaje = get_object_or_404(Viaje, pk=pk)
    else:
        viaje = get_object_or_404(Viaje, pk=pk, conductor=request.user.conductor)

    if request.method == "POST":
        form = ViajeForm(request.POST, instance=viaje, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "El estado del viaje ha sido actualizado.")
            return redirect("viajes:lista_viajes")
    else:
        form = ViajeForm(instance=viaje, user=request.user)

    return render(request, "viajes/formulario.html", {"form": form})


@login_required
@admin_required
def eliminar_viaje(request, pk):
    """
    Elimina un viaje por completo del historial. 
    Restringido únicamente para administradores del sistema.
    """
    viaje = get_object_or_404(Viaje, pk=pk)

    if request.method == "POST":
        viaje.delete()
        messages.success(request, "Viaje eliminado del historial correctamente.")
        return redirect("viajes:lista_viajes")

    return render(
        request,
        "viajes/eliminar.html",
        {"viaje": viaje},
    )