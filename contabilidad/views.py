# contabilidad/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import date, datetime

from .models import Transaccion
from .forms import TransaccionForm                  
from mantenimientos.models import Mantenimiento  
from gastos.models import Gasto 
from viajes.models import Viaje

def normalizar_a_datetime_aware(valor_fecha):
    """
    Convierte de forma segura cualquier tipo de fecha (date, datetime naive o aware)
    en un datetime compatible con la zona horaria del proyecto para ordenamiento.
    """
    if valor_fecha is None:
        return timezone.make_aware(datetime(1970, 1, 1))
    
    # Si es 'date' puro (de un DateField), se convierte a 'datetime' a medianoche
    if isinstance(valor_fecha, date) and not isinstance(valor_fecha, datetime):
        valor_fecha = datetime.combine(valor_fecha, datetime.min.time())
        
    # Si es naive, se le aplica la zona horaria activa de Django
    if timezone.is_naive(valor_fecha):
        return timezone.make_aware(valor_fecha)
        
    return valor_fecha


@login_required
def dashboard_contabilidad(request):
    # 1. Procesar el formulario cuando se guarda una transacción manual
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user  
            transaccion.save()
            return redirect('dashboard_contabilidad')  
    else:
        form = TransaccionForm()

    # 2. Obtener datos de todas las fuentes
    transacciones_manuales = Transaccion.objects.all()
    gastos_externos = Gasto.objects.all()
    mantenimientos = Mantenimiento.objects.all()
    viajes = Viaje.objects.all()

    # 3. Sumar transacciones de la pantalla actual
    ingresos_manuales = transacciones_manuales.filter(tipo__iexact='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
    gastos_manuales = transacciones_manuales.filter(tipo__iexact='gasto').aggregate(Sum('monto'))['monto__sum'] or 0
    
    # 4. Sumar gastos externos
    gastos_viajes = gastos_externos.aggregate(Sum('valor'))['valor__sum'] or 0
    gastos_mantenimiento = mantenimientos.aggregate(Sum('valor'))['valor__sum'] or 0
    
    # 5. Sumar ingresos reales usando el campo 'flete' de Viajes
    ingresos_viajes = viajes.aggregate(Sum('flete'))['flete__sum'] or 0 
    
    # 6. Cálculos finales consolidados
    total_ingresos = ingresos_manuales + ingresos_viajes  
    total_gastos = gastos_manuales + gastos_viajes + gastos_mantenimiento
    balance_total = total_ingresos - total_gastos

    # ==============================================================================
    # 🎯 CREACIÓN DEL HISTORIAL UNIFICADO PARA LA TABLA
    # ==============================================================================
    historial_completo = []

    # A. Agregar transacciones manuales
    for t in transacciones_manuales:
        fecha_original = getattr(t, 'fecha_hora', getattr(t, 'fecha', None))
        historial_completo.append({
            'id_origen': f"T-{t.id:02d}",
            'origen': 'Manual',
            'fecha_hora': normalizar_a_datetime_aware(fecha_original),
            'descripcion': t.descripcion or 'Transacción manual',
            'monto': t.monto,
            'tipo': t.tipo.lower() if t.tipo else 'ingreso',
        })

    # B. Agregar gastos de la app "gastos" (Gastos de viajes)
    for g in gastos_externos:
        desc_gasto = getattr(g, 'descripcion', getattr(g, 'concepto', None)) or str(g)
        historial_completo.append({
            'id_origen': f"G-{g.id:02d}",
            'origen': 'Gastos Viaje',
            'fecha_hora': normalizar_a_datetime_aware(getattr(g, 'fecha', None)),  
            'descripcion': f"Gasto: {desc_gasto}",
            'monto': g.valor,
            'tipo': 'gasto',
        })

    # C. Agregar mantenimientos externos
    for m in mantenimientos:
        desc_maint = getattr(m, 'detalle', getattr(m, 'descripcion', None)) or str(m)
        historial_completo.append({
            'id_origen': f"M-{m.id:02d}",
            'origen': 'Mantenimiento',
            'fecha_hora': normalizar_a_datetime_aware(getattr(m, 'fecha', None)),  
            'descripcion': f"Mantenimiento: {desc_maint}",
            'monto': m.valor,
            'tipo': 'gasto',
        })

    # D. Agregar ingresos por fletes de viajes
    for v in viajes:
        if v.flete and v.flete > 0:
            fecha_original = getattr(v, 'fecha_creacion', getattr(v, 'fecha', None))
            historial_completo.append({
                'id_origen': f"V-{v.id:02d}",
                'origen': 'Viajes (Flete)',
                'fecha_hora': normalizar_a_datetime_aware(fecha_original),  
                'descripcion': f"Flete de viaje: {str(v)}",
                'monto': v.flete,
                'tipo': 'ingreso',
            })

    # Ordenar todo el historial por fecha de forma descendente (el más nuevo primero)
    historial_completo.sort(key=lambda x: x['fecha_hora'], reverse=True)

    context = {
        'transacciones': historial_completo,  
        'form': form,                                             
        'ingresos_totales': total_ingresos,      
        'gastos_totales': total_gastos,          
        'balance_total': balance_total,          
    }
    return render(request, 'contabilidad/dashboard.html', context)