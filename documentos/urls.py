from django.urls import path

from . import views

app_name = "documentos"
urlpatterns = [

    path(
        "",
        views.lista_documentos,
        name="lista_documentos"
    ),

    path(
        "nuevo/",
        views.crear_documento,
        name="crear_documento"
    ),

    path(
        "renovar/<int:pk>/",
        views.renovar_documento,
        name="renovar_documento"
    ),

    path(
        "editar/<int:pk>/",
        views.editar_documento,
        name="editar_documento"
    ),

    path(
        "eliminar/<int:pk>/",
        views.eliminar_documento,
        name="eliminar_documento"
    ),

]