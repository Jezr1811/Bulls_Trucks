from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .forms import LoginForm

from conductores.models import Conductor
from vehiculos.models import Vehiculo
from viajes.models import Viaje
from gastos.models import Gasto
from mantenimientos.models import Mantenimiento
from documentos.models import Documento


def login_view(request):
    if request.user.is_authenticated:
        return redirect("usuarios:dashboard")  # Ajustado al namespace de tu settings.py

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect("usuarios:dashboard")  # Ajustado al namespace de tu settings.py

    return render(
        request,
        "usuarios/login.html",
        {
            "form": form
        }
    )


def logout_view(request):
    logout(request)
    return redirect("usuarios:login")  # Ajustado al namespace de tu settings.py


@login_required  # BLOQUEO: Nadie puede ver métricas sin iniciar sesión primero
def dashboard(request):
    hoy = timezone.now()

    # --- CAPA DE INTELIGENCIA MULTIUSUARIO (ADMIN vs CONDUCTOR) ---
    if request.user.is_superuser:
        # El Administrador ve el panorama global de Bulls Trucks
        total_vehiculos = Vehiculo.objects.count()
        total_conductores = Conductor.objects.count()
        total_viajes = Viaje.objects.count()
        total_mantenimientos = Mantenimiento.objects.count()
        total_documentos = Documento.objects.count()
        total_gastos = Gasto.objects.count()

        ingresos_mes = (
            Viaje.objects.filter(
                fecha_inicio__year=hoy.year,
                fecha_inicio__month=hoy.month
            ).aggregate(total=Sum("flete"))["total"] or 0
        )

        gastos_mes = (
            Gasto.objects.filter(
                fecha__year=hoy.year,
                fecha__month=hoy.month
            ).aggregate(total=Sum("valor"))["total"] or 0
        )

    elif hasattr(request.user, 'conductor'):
        # El Conductor solo ve sus propias métricas de rendimiento y su camión
        conductor_actual = request.user.conductor

        total_vehiculos = Vehiculo.objects.filter(conductor=conductor_actual).count()
        total_conductores = 1  # Solo él mismo
        total_viajes = Viaje.objects.filter(conductor=conductor_actual).count()
        total_mantenimientos = Mantenimiento.objects.filter(vehiculo__conductor=conductor_actual).count()
        total_documentos = Documento.objects.filter(conductor=conductor_actual).count()
        total_gastos = Gasto.objects.filter(viaje__conductor=conductor_actual).count()

        ingresos_mes = (
            Viaje.objects.filter(
                conductor=conductor_actual,
                fecha_inicio__year=hoy.year,
                fecha_inicio__month=hoy.month
            ).aggregate(total=Sum("flete"))["total"] or 0
        )

        gastos_mes = (
            Gasto.objects.filter(
                viaje__conductor=conductor_actual,
                fecha__year=hoy.year,
                fecha__month=hoy.month
            ).aggregate(total=Sum("valor"))["total"] or 0
        )
    else:
        # En caso de un usuario del sistema sin rol asignado, vaciamos las métricas
        total_vehiculos = total_conductores = total_viajes = 0
        total_mantenimientos = total_documentos = total_gastos = 0
        ingresos_mes = gastos_mes = 0

    # El balance se calcula de forma dinámica para ambos roles
    balance_mes = ingresos_mes - gastos_mes

    return render(
        request,
        "dashboard.html",
        {
            "total_vehiculos": total_vehiculos,
            "total_conductores": total_conductores,
            "total_viajes": total_viajes,
            "total_mantenimientos": total_mantenimientos,
            "total_documentos": total_documentos,
            "total_gastos": total_gastos,
            "ingresos_mes": ingresos_mes,
            "gastos_mes": gastos_mes,
            "balance_mes": balance_mes,
        }
    )