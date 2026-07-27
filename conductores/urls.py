from django.urls import path

from . import views

app_name = "conductores"

urlpatterns = [

    path(
        "",
        views.lista_conductores,
        name="lista_conductores"
    ),

    path(
        "nuevo/",
        views.crear_conductor,
        name="crear_conductor"
    ),

    path(
        "editar/<int:pk>/",
        views.editar_conductor,
        name="editar_conductor"
    ),

    path(
        "eliminar/<int:pk>/",
        views.eliminar_conductor,
        name="eliminar_conductor"
    ),

]