from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from foodtrucks.models import FoodTruck
from usuarios.models import PerfilUsuario


def es_administrador(request):

    if not request.user.is_authenticated:
        return False

    if request.user.is_superuser:
        return True

    try:
        perfil = request.user.perfilusuario
        return perfil.rol == 'ADMIN'

    except PerfilUsuario.DoesNotExist:
        return False


def lista_productos(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not es_administrador(request):
        return redirect('lista_ventas')

    buscar = request.GET.get('buscar', '')

    if buscar:
        productos = Producto.objects.filter(
            nombre__icontains=buscar
        )
    else:
        productos = Producto.objects.all()

    contexto = {
        'productos': productos,
        'buscar': buscar,
    }

    return render(
        request,
        'productos/lista.html',
        contexto
    )


def crear_producto(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not es_administrador(request):
        return redirect('lista_ventas')

    foodtrucks = FoodTruck.objects.all()

    if request.method == 'POST':

        Producto.objects.create(
            foodtruck_id=request.POST['foodtruck'],
            nombre=request.POST['nombre'],
            precio=request.POST['precio'],
            stock=request.POST['stock']
        )

        return redirect('lista_productos')

    contexto = {
        'foodtrucks': foodtrucks
    }

    return render(
        request,
        'productos/formulario.html',
        contexto
    )


def editar_producto(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not es_administrador(request):
        return redirect('lista_ventas')

    producto = get_object_or_404(
        Producto,
        id=id
    )

    foodtrucks = FoodTruck.objects.all()

    if request.method == 'POST':

        producto.foodtruck_id = request.POST['foodtruck']
        producto.nombre = request.POST['nombre']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']

        producto.save()

        return redirect('lista_productos')

    contexto = {
        'producto': producto,
        'foodtrucks': foodtrucks
    }

    return render(
        request,
        'productos/formulario.html',
        contexto
    )


def eliminar_producto(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not es_administrador(request):
        return redirect('lista_ventas')

    producto = get_object_or_404(
        Producto,
        id=id
    )

    producto.delete()

    return redirect('lista_productos')