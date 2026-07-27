from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Vehiculo
from .forms import VehiculoForm
# Importamos el decorador personalizado desde tu app usuarios
from usuarios.decorators import admin_required

@login_required
def lista_vehiculos(request):
    # --- CAPA DE FILTRADO MULTIUSUARIO ---
    if request.user.is_superuser:
        # El administrador ve absolutamente toda la flota de la empresa
        vehiculos = Vehiculo.objects.all()
    elif hasattr(request.user, 'conductor'):
        # El conductor solo ve el o los vehículos que tiene vinculados
        vehiculos = Vehiculo.objects.filter(conductor=request.user.conductor)
    else:
        # Seguridad: si no es admin ni tiene perfil de conductor, no ve nada
        vehiculos = Vehiculo.objects.none()

    return render(
        request,
        "vehiculos/lista.html",
        {"vehiculos": vehiculos},
    )

@login_required
@admin_required  # BLOQUEO TOTAL: Solo el administrador puede registrar nuevos vehículos
def crear_vehiculo(request):
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nuevo vehículo registrado con éxito en la flota.")
            return redirect("vehiculos:lista_vehiculos")
    else:
        form = VehiculoForm()

    return render(
        request,
        "vehiculos/formulario.html",
        {"form": form},
    )

@login_required
def editar_vehiculo(request, pk):
    # --- CAPA DE SEGURIDAD EN URL (ID HACKING) ---
    if request.user.is_superuser:
        # El administrador puede buscar y editar cualquier vehículo
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
    else:
        # El conductor solo puede buscar y editar el vehículo asignado a él
        vehiculo = get_object_or_404(Vehiculo, pk=pk, conductor=request.user.conductor)

    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos del vehículo han sido actualizados.")
            return redirect("vehiculos:lista_vehiculos")
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(
        request,
        "vehiculos/formulario.html",
        {"form": form},
    )

@login_required
@admin_required  # BLOQUEO TOTAL: Un conductor jamás debe poder eliminar un vehículo de la empresa
def eliminar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == "POST":
        vehiculo.delete()
        messages.success(request, "Vehículo eliminado de la flota correctamente.")
        return redirect("vehiculos:lista_vehiculos")

    return render(
        request,
        "vehiculos/eliminar.html",
        {"vehiculo": vehiculo},
    )