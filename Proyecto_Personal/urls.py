from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("usuarios.urls")),
    path("vehiculos/", include("vehiculos.urls")),
    path("conductores/", include("conductores.urls")),
    path("trailers/", include("trailers.urls")),
    path("viajes/", include("viajes.urls")),
    path("documentos/", include("documentos.urls")),
    path("mantenimientos/", include("mantenimientos.urls")),
    path("gastos/", include("gastos.urls")),
    path("contabilidad/", include("contabilidad.urls")),
    path("reportes/", include("reportes.urls")),
]