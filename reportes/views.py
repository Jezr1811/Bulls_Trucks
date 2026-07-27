from django.shortcuts import render
from django.db.models import Sum, Avg, F, Count
from viajes.models import Viaje  
from mantenimientos.models import Mantenimiento  
from conductores.models import Conductor
from documentos.models import Documento

# =========================================================================
# 1. REPORTE DE VIAJES
# =========================================================================
def reporte_viajes(request):
    """
    Vista para el reporte de viajes utilizando los campos reales del modelo.
    """
    viajes = Viaje.objects.all().order_by('-fecha_creacion')
    total_viajes = viajes.count()
    ganancias_semanales = viajes.aggregate(total=Sum('flete'))['total'] or 0
    ganancia_promedio = viajes.aggregate(promedio=Avg('flete'))['promedio'] or 0
    
    viajes_con_fechas = viajes.filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)
    duracion_total_delta = viajes_con_fechas.aggregate(
        total=Sum(F('fecha_fin') - F('fecha_inicio'))
    )['total']
    
    duracion_total = duracion_total_delta.days if duracion_total_delta else 0

    context = {
        'viajes': viajes,
        'total_viajes': total_viajes,
        'ganancias_semanales': ganancias_semanales,
        'duracion_total': duracion_total,
        'ganancia_promedio': ganancia_promedio,
    }
    return render(request, 'reportes/reporte_viajes.html', context)


# =========================================================================
# 2. REPORTE DE MANTENIMIENTO
# =========================================================================
def reporte_mantenimiento(request):
    """
    Vista para el reporte de mantenimientos utilizando los campos reales del modelo.
    """
    mantenimientos = Mantenimiento.objects.all().order_by('-fecha')
    total_mantenimientos = mantenimientos.count()
    costo_total = mantenimientos.aggregate(total=Sum('valor'))['total'] or 0
    costo_promedio = mantenimientos.aggregate(promedio=Avg('valor'))['promedio'] or 0
    
    mantenimientos_vehiculos = mantenimientos.filter(vehiculo__isnull=False).count()
    mantenimientos_trailers = mantenimientos.filter(trailer__isnull=False).count()

    context = {
        'mantenimientos': mantenimientos,
        'total_mantenimientos': total_mantenimientos,
        'costo_total': costo_total,
        'costo_promedio': costo_promedio,
        'mantenimientos_vehiculos': mantenimientos_vehiculos,
        'mantenimientos_trailers': mantenimientos_trailers,
    }
    return render(request, 'reportes/reporte_mantenimiento.html', context)


# =========================================================================
# 3. REPORTE DE CONDUCTORES (NUEVO & REAL)
# =========================================================================
def reporte_conductores(request):

    conductores = Conductor.objects.annotate(
        total_viajes=Count("viaje"),
        total_ingresos=Sum("viaje__flete"),
    ).order_by("-total_viajes")

    for conductor in conductores:

        conductor.documento_licencia = Documento.objects.filter(
            conductor=conductor,
            tipo="licencia"
        ).first()

    context = {

        "conductores_stats": conductores,

        "total_viajes_operadores": Viaje.objects.count(),

        "ingresos_totales": Viaje.objects.aggregate(
            total=Sum("flete")
        )["total"] or 0,

        "total_incidentes": 0,

    }

    return render(
        request,
        "reportes/reporte_conductores.html",
        context,
    )