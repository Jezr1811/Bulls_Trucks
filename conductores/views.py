from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from usuarios.decorators import admin_required
from documentos.models import Documento

from .models import Conductor
from .forms import ConductorForm


@login_required
@admin_required
def lista_conductores(request):
    buscar = request.GET.get("buscar", "").strip()
    estado = request.GET.get("estado", "").strip()

    conductores_qs = Conductor.objects.all().order_by("-id")

    if buscar:
        conductores_qs = conductores_qs.filter(
            Q(nombre__icontains=buscar) |
            Q(correo__icontains=buscar) |
            Q(telefono__icontains=buscar)
        )

    if estado in ["activo", "inactivo"]:
        conductores_qs = conductores_qs.filter(estado=estado)

    conductores = list(conductores_qs)

    licencias = Documento.objects.filter(
        conductor__in=conductores,
        tipo="licencia"
    ).select_related("conductor")

    licencias_por_conductor = {doc.conductor_id: doc for doc in licencias}

    for conductor in conductores:
        conductor.documento_licencia = licencias_por_conductor.get(conductor.id)

    return render(
        request,
        "conductores/lista.html",
        {
            "conductores": conductores,
        },
    )


@login_required
@admin_required
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
        "editar": False,
    },
)


@login_required
@admin_required
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
        "editar": True,
    },
)


@login_required
@admin_required
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