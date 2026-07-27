from django.urls import path
from . import views

# Este es el app_name que usamos en el menú desplegable (contabilidad:)
app_name = "contabilidad"

urlpatterns = [
    path(
        "", 
        views.dashboard_contabilidad, 
        name="dashboard_contabilidad"
    ),
]