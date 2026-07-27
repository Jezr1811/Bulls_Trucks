from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Mantenimiento
from .forms import MantenimientoForm
from usuarios.decorators import admin_required


@login_required
def lista_mantenimientos(request):
    """
    Muestra el historial técnico de mantenimientos.
    - Superusuario: ve toda la flota.
    - Conductor: solo ve su camión asignado.
    """
    if request.user.is_superuser:
        mantenimientos = Mantenimiento.objects.all().order_by("-id")
    elif hasattr(request.user, 'conductor'):
        mantenimientos = Mantenimiento.objects.filter(
            vehiculo__conductor=request.user.conductor
        ).order_by("-id")
    else:
        mantenimientos = Mantenimiento.objects.none()

    return render(
        request,
        "mantenimientos/lista.html",
        {"mantenimientos": mantenimientos}
    )


@login_required
def crear_mantenimiento(request):
    """
    Registra un nuevo mantenimiento validando los datos mediante MantenimientoForm.
    """
    if request.method == "POST":
        form = MantenimientoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro de mantenimiento guardado con éxito.")
            return redirect("mantenimientos:lista_mantenimientos")
    else:
        form = MantenimientoForm(user=request.user)

    return render(
        request,
        "mantenimientos/formulario.html",
        {"form": form}
    )


@login_required
def detalle_mantenimiento(request, pk):
    """
    Muestra la información técnica detallada y la evidencia fotográfica de un registro.
    """
    if request.user.is_superuser:
        mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    else:
        mantenimiento = get_object_or_404(
            Mantenimiento, 
            pk=pk, 
            vehiculo__conductor=request.user.conductor
        )
        
    return render(
        request, 
        "mantenimientos/detalle.html", 
        {"mantenimiento": mantenimiento}
    )


@login_required
def editar_mantenimiento(request, pk):
    """
    Permite modificar un registro existente protegiendo contra manipulación de IDs en la URL.
    """
    if request.user.is_superuser:
        mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    else:
        mantenimiento = get_object_or_404(
            Mantenimiento, 
            pk=pk, 
            vehiculo__conductor=request.user.conductor
        )

    if request.method == "POST":
        form = MantenimientoForm(
            request.POST, 
            request.FILES, 
            instance=mantenimiento, 
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "El registro de mantenimiento ha sido actualizado.")
            return redirect("mantenimientos:lista_mantenimientos")
    else:
        form = MantenimientoForm(instance=mantenimiento, user=request.user)

    return render(
        request,
        "mantenimientos/formulario.html",
        {"form": form, "mantenimiento": mantenimiento}
    )


@login_required
@admin_required
def eliminar_mantenimiento(request, pk):
    """
    Elimina un registro de la base de datos de manera definitiva. Acceso exclusivo para administradores.
    """
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)

    if request.method == "POST":
        mantenimiento.delete()
        messages.success(request, "Registro de mantenimiento eliminado correctamente.")
        return redirect("mantenimientos:lista_mantenimientos")

    return render(
        request,
        "mantenimientos/eliminar.html",
        {"mantenimiento": mantenimiento}
    )