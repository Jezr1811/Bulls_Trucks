from django.urls import path

from .views import (
    dashboard,
    login_view,
    logout_view,
    lista_usuarios,
    crear_usuario,
    editar_usuario,
    activar_usuario,
    desactivar_usuario,
)

app_name = "usuarios"

urlpatterns = [

    path(
        "login/",
        login_view,
        name="login"
    ),

    path(
        "logout/",
        logout_view,
        name="logout"
    ),

    path(
        "",
        dashboard,
        name="dashboard"
    ),

    path(
        "usuarios/",
        lista_usuarios,
        name="lista_usuarios"
    ),

    path(
        "usuarios/nuevo/",
        crear_usuario,
        name="crear_usuario"
    ),

    path(
        "usuarios/<int:pk>/editar/",
        editar_usuario,
        name="editar_usuario"
    ),

    path(
        "usuarios/<int:pk>/desactivar/",
        desactivar_usuario,
        name="desactivar_usuario"
    ),
    
    
    path(
        "usuarios/<int:pk>/activar/",
        activar_usuario,
        name="activar_usuario"
    ),



]