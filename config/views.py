from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta, datetime

from foodtrucks.models import FoodTruck
from productos.models import Producto
from ventas.models import Venta


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    hoy = timezone.localdate()

    periodo = request.GET.get(
        'periodo',
        'todo'
    )

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

        fecha_hasta = (
            primer_dia_mes - timedelta(days=1)
        )

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


    ventas = Venta.objects.all()

    if fecha_desde:

        ventas = ventas.filter(
            fecha__date__gte=fecha_desde
        )

    if fecha_hasta:

        ventas = ventas.filter(
            fecha__date__lte=fecha_hasta
        )


    total_foodtrucks = FoodTruck.objects.count()

    total_productos = Producto.objects.count()

    total_ventas = ventas.count()

    total_vendido = sum(
        venta.total
        for venta in ventas
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

        'total_foodtrucks': total_foodtrucks,

        'total_productos': total_productos,

        'total_ventas': total_ventas,

        'total_vendido': total_vendido,

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
        'dashboard.html',
        contexto
    )