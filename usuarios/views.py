from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import PerfilUsuario


def iniciar_sesion(request):

    if request.user.is_authenticated:

        try:
            perfil = request.user.perfilusuario

            if perfil.rol == 'ADMIN':
                return redirect('dashboard')

            return redirect('lista_ventas')

        except PerfilUsuario.DoesNotExist:

            return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            perfil, creado = PerfilUsuario.objects.get_or_create(
                usuario=usuario
            )

            if usuario.is_superuser:

                perfil.rol = 'ADMIN'
                perfil.activo = True
                perfil.save()

            elif creado:

                perfil.rol = 'CAJERO'
                perfil.activo = True
                perfil.save()

            if not perfil.activo:

                messages.error(
                    request,
                    'Este usuario se encuentra deshabilitado.'
                )

                return redirect('login')

            login(request, usuario)

            if perfil.rol == 'ADMIN':
                return redirect('dashboard')

            return redirect('lista_ventas')

        else:

            messages.error(
                request,
                'Usuario o contraseña incorrectos.'
            )

    return render(
        request,
        'usuarios/login.html'
    )


def cerrar_sesion(request):

    logout(request)

    return redirect('login')


def lista_cajeros(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:

        try:

            perfil = request.user.perfilusuario

            if perfil.rol != 'ADMIN':
                return redirect('lista_ventas')

        except PerfilUsuario.DoesNotExist:

            return redirect('lista_ventas')

    cajeros = PerfilUsuario.objects.filter(
        rol='CAJERO'
    ).select_related('usuario')

    return render(
        request,
        'usuarios/cajeros.html',
        {
            'cajeros': cajeros
        }
    )


def crear_cajero(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:

        try:

            perfil = request.user.perfilusuario

            if perfil.rol != 'ADMIN':
                return redirect('lista_ventas')

        except PerfilUsuario.DoesNotExist:

            return redirect('lista_ventas')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Ese nombre de usuario ya existe.'
            )

            return redirect('crear_cajero')

        usuario = User.objects.create_user(
            username=username,
            password=password
        )

        PerfilUsuario.objects.create(
            usuario=usuario,
            rol='CAJERO',
            activo=True
        )

        messages.success(
            request,
            'Cajero creado correctamente.'
        )

        return redirect('lista_cajeros')

    return render(
        request,
        'usuarios/crear_cajero.html'
    )


def cambiar_estado_cajero(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:

        try:

            perfil = request.user.perfilusuario

            if perfil.rol != 'ADMIN':
                return redirect('lista_ventas')

        except PerfilUsuario.DoesNotExist:

            return redirect('lista_ventas')

    perfil_cajero = PerfilUsuario.objects.get(
        id=id,
        rol='CAJERO'
    )

    perfil_cajero.activo = not perfil_cajero.activo

    perfil_cajero.save()

    return redirect('lista_cajeros')


def eliminar_cajero(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:

        try:

            perfil = request.user.perfilusuario

            if perfil.rol != 'ADMIN':
                return redirect('lista_ventas')

        except PerfilUsuario.DoesNotExist:

            return redirect('lista_ventas')

    perfil_cajero = PerfilUsuario.objects.get(
        id=id,
        rol='CAJERO'
    )

    usuario = perfil_cajero.usuario

    usuario.delete()

    messages.success(
        request,
        'Cajero eliminado correctamente.'
    )

    return redirect('lista_cajeros')