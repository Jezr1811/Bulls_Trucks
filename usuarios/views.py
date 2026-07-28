from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.db.models import Sum
from django.utils import timezone
from .forms import LoginForm, UsuarioRegistroForm
from conductores.models import Conductor
from vehiculos.models import Vehiculo
from viajes.models import Viaje
from gastos.models import Gasto
from mantenimientos.models import Mantenimiento
from documentos.models import Documento
from django.contrib import messages
from django.contrib.auth.models import User
from usuarios.decorators import admin_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

def login_view(request):
    if request.user.is_authenticated:
        return redirect("usuarios:dashboard")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect("usuarios:dashboard")

    return render(
        request,
        "usuarios/login.html",
        {
            "form": form
        }
    )


def logout_view(request):
    logout(request)
    return redirect("usuarios:login")


@login_required
def dashboard(request):
    hoy = timezone.now()

    if request.user.is_superuser:
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

    else:
        try:
            conductor_actual = request.user.conductor
        except Conductor.DoesNotExist:
            total_vehiculos = 0
            total_conductores = 0
            total_viajes = 0
            total_mantenimientos = 0
            total_documentos = 0
            total_gastos = 0
            ingresos_mes = 0
            gastos_mes = 0
        else:
            total_vehiculos = Vehiculo.objects.filter(conductor=conductor_actual).count()
            total_conductores = 1
            total_viajes = Viaje.objects.filter(conductor=conductor_actual).count()
            total_mantenimientos = Mantenimiento.objects.filter(
                vehiculo__conductor=conductor_actual
            ).count()
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
    
@login_required
@admin_required
def crear_usuario(request):

    if request.method == "POST":

        form = UsuarioRegistroForm(request.POST)

        if form.is_valid():

            usuario = form.save(commit=False)

            if form.cleaned_data["tipo_usuario"] == "admin":
                usuario.is_staff = True
                usuario.is_superuser = True

            usuario.save()

            if form.cleaned_data["tipo_usuario"] == "conductor":

                Conductor.objects.create(
                    usuario=usuario,
                    nombre=form.cleaned_data["nombre_conductor"],
                    telefono=form.cleaned_data["telefono"],
                    correo=form.cleaned_data["correo_conductor"],
                )

            messages.success(request, "Usuario creado correctamente.")

            return redirect("usuarios:crear_usuario")

    else:

        form = UsuarioRegistroForm()

    return render(
        request,
        "usuarios/crear_usuario.html",
        {
            "form": form,
        },
    )
    
    
@login_required
@admin_required
def lista_usuarios(request):

    usuarios = User.objects.all().order_by("username")

    return render(
        request,
        "usuarios/lista_usuarios.html",
        {
            "usuarios": usuarios,
        },
    )
    
    
@login_required
@admin_required
def editar_usuario(request, pk):

    usuario = User.objects.get(pk=pk)

    if request.method == "POST":

        form = UsuarioRegistroForm(request.POST, instance=usuario)

        if form.is_valid():

            usuario = form.save(commit=False)

            if form.cleaned_data["tipo_usuario"] == "admin":
                usuario.is_staff = True
                usuario.is_superuser = True

            else:
                usuario.is_staff = False
                usuario.is_superuser = False

            usuario.save()

            messages.success(request, "Usuario actualizado correctamente.")

            return redirect("usuarios:lista_usuarios")

    else:

        initial = {
            "tipo_usuario": "admin" if usuario.is_superuser else "conductor"
        }

        form = UsuarioRegistroForm(instance=usuario, initial=initial)

    return render(
        request,
        "usuarios/crear_usuario.html",
        {
            "form": form,
            "editar": True,
        },
    )

@login_required
@admin_required
def desactivar_usuario(request, usuario_id):

    usuario = User.objects.get(id=usuario_id)

    usuario.is_active = False
    usuario.save()

    return redirect("usuarios:lista_usuarios")
    

# @login_required
@admin_required
def activar_usuario(request, usuario_id):

    try:
        usuario = User.objects.get(id=usuario_id)
        usuario.is_active = True
        usuario.save()

        messages.success(request, "Usuario activado correctamente.")

        return redirect("usuarios:lista_usuarios")

    except Exception as e:
        return HttpResponse(str(e))