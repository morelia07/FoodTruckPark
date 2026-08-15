from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodTruck
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


def lista_foodtrucks(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not es_administrador(request):
        return redirect('lista_ventas')

    busqueda = request.GET.get('buscar', '')

    if busqueda:
        foodtrucks = FoodTruck.objects.filter(
            nombre__icontains=busqueda
        )
    else:
        foodtrucks = FoodTruck.objects.all()

    contexto = {
        'foodtrucks': foodtrucks,
        'busqueda': busqueda,
    }

    return render(
        request,
        'foodtrucks/lista.html',
        contexto
    )


def crear_foodtruck(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not es_administrador(request):
        return redirect('lista_ventas')

    if request.method == 'POST':

        FoodTruck.objects.create(
            nombre=request.POST['nombre'],
            propietario=request.POST['propietario'],
            tipo_comida=request.POST['tipo_comida'],
            estado=request.POST.get('estado') == 'on'
        )

        return redirect('lista_foodtrucks')

    return render(
        request,
        'foodtrucks/formulario.html'
    )


def editar_foodtruck(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not es_administrador(request):
        return redirect('lista_ventas')

    foodtruck = get_object_or_404(
        FoodTruck,
        id=id
    )

    if request.method == 'POST':

        foodtruck.nombre = request.POST['nombre']
        foodtruck.propietario = request.POST['propietario']
        foodtruck.tipo_comida = request.POST['tipo_comida']
        foodtruck.estado = request.POST.get('estado') == 'on'

        foodtruck.save()

        return redirect('lista_foodtrucks')

    contexto = {
        'foodtruck': foodtruck
    }

    return render(
        request,
        'foodtrucks/formulario.html',
        contexto
    )


def eliminar_foodtruck(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not es_administrador(request):
        return redirect('lista_ventas')

    foodtruck = get_object_or_404(
        FoodTruck,
        id=id
    )

    foodtruck.delete()

    return redirect('lista_foodtrucks')

