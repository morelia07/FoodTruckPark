from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

from ventas.models import DetalleVenta


def reporte_ventas(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:

        try:
            if request.user.perfilusuario.rol != 'ADMIN':
                return redirect('lista_ventas')

        except:
            return redirect('lista_ventas')

    hoy = timezone.localdate()

    periodo = request.GET.get('periodo', 'todo')

    fecha_desde = None
    fecha_hasta = hoy

    if periodo == 'hoy':

        fecha_desde = hoy

    elif periodo == '7':

        fecha_desde = hoy - timedelta(days=6)

    elif periodo == '30':

        fecha_desde = hoy - timedelta(days=29)

    elif periodo == 'mes':

        fecha_desde = hoy.replace(day=1)

    elif periodo == 'anterior':

        primer_dia_mes = hoy.replace(day=1)

        fecha_hasta = primer_dia_mes - timedelta(days=1)

        fecha_desde = fecha_hasta.replace(day=1)

    elif periodo == 'personalizado':

        fecha_desde_texto = request.GET.get(
            'fecha_desde'
        )

        fecha_hasta_texto = request.GET.get(
            'fecha_hasta'
        )

        if fecha_desde_texto:
            fecha_desde = datetime.strptime(
                fecha_desde_texto,
                '%Y-%m-%d'
            ).date()

        if fecha_hasta_texto:
            fecha_hasta = datetime.strptime(
                fecha_hasta_texto,
                '%Y-%m-%d'
            ).date()

    detalles = DetalleVenta.objects.all()

    if fecha_desde:
        detalles = detalles.filter(
            venta__fecha__date__gte=fecha_desde
        )

    if fecha_hasta:
        detalles = detalles.filter(
            venta__fecha__date__lte=fecha_hasta
        )

    detalles = (
        detalles
        .values(
            'producto__foodtruck__nombre',
            'producto__nombre'
        )
        .annotate(
            cantidad_total=Sum('cantidad'),
            total_generado=Sum(
                ExpressionWrapper(
                    F('cantidad') * F('precio'),
                    output_field=DecimalField(
                        max_digits=10,
                        decimal_places=2
                    )
                )
            )
        )
        .order_by(
            'producto__foodtruck__nombre',
            'producto__nombre'
        )
    )

    totales_foodtruck = {}

    for detalle in detalles:

        foodtruck = detalle[
            'producto__foodtruck__nombre'
        ]

        if foodtruck not in totales_foodtruck:
            totales_foodtruck[foodtruck] = 0

        totales_foodtruck[foodtruck] += (
            detalle['total_generado']
        )

    total_general = sum(
        totales_foodtruck.values()
    )

    nombres_periodos = {
        'hoy': 'Hoy',
        '7': 'Últimos 7 días',
        '30': 'Últimos 30 días',
        'mes': 'Este mes',
        'anterior': 'Mes anterior',
        'personalizado': 'Período personalizado',
        'todo': 'Todo'
    }

    contexto = {
        'detalles': detalles,
        'totales_foodtruck': totales_foodtruck,
        'total_general': total_general,
        'periodo': periodo,
        'nombre_periodo': nombres_periodos.get(
            periodo,
            'Todo'
        ),
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    }

    return render(
        request,
        'reportes/ventas.html',
        contexto
    )