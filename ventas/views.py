from django.shortcuts import render, redirect, get_object_or_404

from .models import Venta, DetalleVenta
from productos.models import Producto


def lista_ventas(request):

    if request.user.is_superuser:
        ventas = Venta.objects.all()

    else:
        ventas = Venta.objects.filter(
            cajero=request.user
        )

    ventas = ventas.select_related(
        'cajero'
    ).order_by('-fecha')

    for venta in ventas:

        detalles = DetalleVenta.objects.filter(
            venta=venta
        ).select_related('foodtruck')

        foodtrucks = []
        ids_foodtrucks = set()

        for detalle in detalles:

            if detalle.foodtruck.id not in ids_foodtrucks:

                foodtrucks.append(
                    detalle.foodtruck
                )

                ids_foodtrucks.add(
                    detalle.foodtruck.id
                )

        venta.foodtrucks_unicos = foodtrucks

    contexto = {
        'ventas': ventas
    }

    return render(
        request,
        'ventas/lista.html',
        contexto
    )


def crear_venta(request):

    productos = Producto.objects.all()

    if request.method == 'POST':

        metodo_pago = request.POST['metodo_pago']

        productos_seleccionados = request.POST.getlist(
            'productos'
        )

        total = 0

        venta = Venta.objects.create(
            metodo_pago=metodo_pago,
            total=0,
            cajero=request.user
        )

        for producto_id in productos_seleccionados:

            producto = get_object_or_404(
                Producto,
                id=producto_id
            )

            cantidad = int(
                request.POST.get(
                    f'cantidad_{producto.id}',
                    1
                )
            )

            subtotal = producto.precio * cantidad

            total += subtotal

            DetalleVenta.objects.create(
                venta=venta,
                foodtruck=producto.foodtruck,
                producto=producto,
                cantidad=cantidad,
                precio=producto.precio
            )

            producto.stock -= cantidad

            producto.save()

        venta.total = total
        venta.save()

        return redirect('lista_ventas')

    contexto = {
        'productos': productos
    }

    return render(
        request,
        'ventas/formulario.html',
        contexto
    )


def detalle_venta(request, id):

    venta = get_object_or_404(
        Venta,
        id=id
    )

    if not request.user.is_superuser:

        if venta.cajero != request.user:
            return redirect('lista_ventas')

    detalles = DetalleVenta.objects.filter(
        venta=venta
    ).select_related(
        'foodtruck',
        'producto'
    )

    contexto = {
        'venta': venta,
        'detalles': detalles
    }

    return render(
        request,
        'ventas/detalle.html',
        contexto
    )