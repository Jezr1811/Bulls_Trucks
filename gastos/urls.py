from django.urls import path

from . import views

app_name = "gastos"

urlpatterns = [
    path(
        "",
        views.lista_gastos,
        name="lista_gastos"
    ),

    # 🛠️ CORRECCIÓN: Agregamos <int:viaje_id> y cambiamos el name a "registrar_gasto"
    path(
        "viaje/<int:viaje_id>/nuevo/",
        views.crear_gasto,
        name="registrar_gasto"
    ),

    path(
        "editar/<int:pk>/",
        views.editar_gasto,
        name="editar_gasto"
    ),

    path(
        "eliminar/<int:pk>/",
        views.eliminar_gasto,
        name="eliminar_gasto"
    ),
]