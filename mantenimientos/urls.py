from django.urls import path

from . import views

app_name = "mantenimientos"

urlpatterns = [

    path(
        "",
        views.lista_mantenimientos,
        name="lista_mantenimientos"
    ),

    path(
        "nuevo/",
        views.crear_mantenimiento,
        name="crear_mantenimiento"
    ),

    # 🔍 AGREGAMOS ESTA RUTA PARA EL DETALLE
    path(
        "<int:pk>/",
        views.detalle_mantenimiento,
        name="detalle_mantenimiento"
    ),

    path(
        "editar/<int:pk>/",
        views.editar_mantenimiento,
        name="editar_mantenimiento"
    ),

    path(
        "eliminar/<int:pk>/",
        views.eliminar_mantenimiento,
        name="eliminar_mantenimiento"
    ),

]