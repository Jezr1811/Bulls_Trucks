from django.urls import path
from . import views

app_name = "trailers"

urlpatterns = [

    path(
        "",
        views.lista_trailers,
        name="lista_trailers"
    ),

    path(
        "nuevo/",
        views.crear_trailer,
        name="crear_trailer"
    ),

    path(
        "editar/<int:pk>/",
        views.editar_trailer,
        name="editar_trailer"
    ),

    path(
        "eliminar/<int:pk>/",
        views.eliminar_trailer,
        name="eliminar_trailer"
    ),
]