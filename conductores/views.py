from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Conductor
from .forms import ConductorForm
# Importamos el decorador personalizado para restringir el acceso total a conductores
from usuarios.decorators import admin_required


@login_required
@admin_required  # BLOQUEO TOTAL: Solo el administrador puede auditar la nómina de conductores
def lista_conductores(request):
    conductores = Conductor.objects.all().order_by("-id")

    return render(
        request,
        "conductores/lista.html",
        {
            "conductores": conductores,
        },
    )


@login_required
@admin_required  # BLOQUEO TOTAL: Registrar nuevos empleados es una tarea puramente administrativa
def crear_conductor(request):
    if request.method == "POST":
        form = ConductorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Nuevo conductor registrado con éxito en la empresa.")
            return redirect("conductores:lista_conductores")
    else:
        form = ConductorForm()

    return render(
        request,
        "conductores/formulario.html",
        {
            "form": form,
        },
    )


@login_required
@admin_required  # BLOQUEO TOTAL: Modificar licencias o estados críticos es solo para el Administrador
def editar_conductor(request, pk):
    conductor = get_object_or_404(Conductor, pk=pk)

    if request.method == "POST":
        form = ConductorForm(request.POST, instance=conductor)

        if form.is_valid():
            form.save()
            messages.success(request, f"Los datos de {conductor.nombre} han sido actualizados.")
            return redirect("conductores:lista_conductores")
    else:
        form = ConductorForm(instance=conductor)

    return render(
        request,
        "conductores/formulario.html",
        {
            "form": form,
            "conductor": conductor,
        },
    )


@login_required
@admin_required  # BLOQUEO TOTAL: Desvincular un conductor es una acción crítica protegida
def eliminar_conductor(request, pk):
    conductor = get_object_or_404(Conductor, pk=pk)

    if request.method == "POST":
        nombre_conductor = conductor.nombre
        conductor.delete()
        messages.success(request, f"El conductor {nombre_conductor} ha sido dado de baja correctamente.")
        return redirect("conductores:lista_conductores")

    return render(
        request,
        "conductores/eliminar.html",
        {
            "conductor": conductor,
        },
    )