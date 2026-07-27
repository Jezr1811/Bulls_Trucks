from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Gasto
from .forms import GastoForm
from viajes.models import Viaje  # 👈 Importamos Viaje para amarrar el contexto
from usuarios.decorators import admin_required


@login_required
def lista_gastos(request):
    # --- CAPA DE FILTRADO MULTIUSUARIO ---
    if request.user.is_superuser:
        gastos = Gasto.objects.all().order_by("-id")
    elif hasattr(request.user, 'conductor'):
        gastos = Gasto.objects.filter(viaje__conductor=request.user.conductor).order_by("-id")
    else:
        gastos = Gasto.objects.none()

    return render(
        request, 
        "gastos/lista.html", 
        {"gastos": gastos}
    )


@login_required
def crear_gasto(request, viaje_id):  # 👈 Ahora recibe el viaje_id desde la URL
    # Validamos que el viaje exista y que pertenezca al conductor (si no es admin)
    if request.user.is_superuser:
        viaje = get_object_or_404(Viaje, pk=viaje_id)
    else:
        viaje = get_object_or_404(Viaje, pk=viaje_id, conductor=request.user.conductor)

    if request.method == "POST":
        # Agregamos request.FILES para soportar la carga del Recibo/Foto de tu maqueta
        form = GastoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.viaje = viaje  # 👈 Vinculamos el gasto automáticamente al viaje actual
            gasto.save()
            messages.success(request, f"Gasto de {gasto.get_tipo_display()} registrado con éxito.")
            # Redirigimos al detalle del viaje para que vea el gasto sumado de inmediato
            return redirect("viajes:detalle_viaje", pk=viaje.id)
    else:
        form = GastoForm(user=request.user)

    return render(
        request, 
        "gastos/registrar_gasto.html",  # 👈 Apunta a tu plantilla estilizada
        {"form": form, "viaje": viaje}   # Enviamos 'viaje' para renderizar el resumen inferior
    )


@login_required
def editar_gasto(request, pk):
    # --- CAPA DE SEGURIDAD EN URL (ID HACKING) ---
    if request.user.is_superuser:
        gasto = get_object_or_404(Gasto, pk=pk)
    else:
        gasto = get_object_or_404(Gasto, pk=pk, viaje__conductor=request.user.conductor)

    viaje = gasto.viaje  # Recuperamos el viaje para mantener el diseño del historial abajo

    if request.method == "POST":
        form = GastoForm(request.POST, request.FILES, instance=gasto, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "El registro del gasto ha sido modificado.")
            return redirect("viajes:detalle_viaje", pk=viaje.id)
    else:
        form = GastoForm(instance=gasto, user=request.user)

    return render(
        request, 
        "gastos/registrar_gasto.html", 
        {"form": form, "viaje": viaje}
    )


@login_required
@admin_required
def eliminar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)
    viaje_id = gasto.viaje.id  # Guardamos la ID para saber a dónde regresar

    if request.method == "POST":
        gasto.delete()
        messages.success(request, "El gasto ha sido eliminado de la contabilidad.")
        return redirect("viajes:detalle_viaje", pk=viaje_id)

    return render(
        request, 
        "gastos/eliminar.html", 
        {"gasto": gasto}
    )