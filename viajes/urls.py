from django.urls import path
from . import views

app_name = "viajes"

urlpatterns = [
    path(
        "",
        views.lista_viajes,
        name="lista_viajes"
    ),
    path(
        "nuevo/",
        views.crear_viaje,
        name="crear_viaje"
    ),
    # 🔗 Nueva ruta: Menú interno al dar clic a la tarjeta del viaje
    path(
        "<int:pk>/",
        views.detalle_viaje,
        name="detalle_viaje"
    ),
    # 🔗 Nueva ruta: Botones dinámicos de Iniciar y Terminar viaje
    path(
        "<int:pk>/estado/<str:accion>/",
        views.cambiar_estado_viaje,
        name="cambiar_estado"
    ),
    path(
        "editar/<int:pk>/",
        views.editar_viaje,
        name="editar_viaje"
    ),
    path(
        "eliminar/<int:pk>/",
        views.eliminar_viaje,
        name="eliminar_viaje"
    ),
]