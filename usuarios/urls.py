from django.urls import path

from .views import (
    iniciar_sesion,
    cerrar_sesion,
    lista_cajeros,
    crear_cajero,
    cambiar_estado_cajero,
    eliminar_cajero,
)


urlpatterns = [

    # Login
    path(
        '',
        iniciar_sesion,
        name='login'
    ),

    # Cerrar sesión
    path(
        'logout/',
        cerrar_sesion,
        name='logout'
    ),

    # Lista de cajeros
    path(
        'cajeros/',
        lista_cajeros,
        name='lista_cajeros'
    ),

    # Crear cajero
    path(
        'cajeros/nuevo/',
        crear_cajero,
        name='crear_cajero'
    ),

    # Activar o deshabilitar cajero
    path(
        'cajeros/estado/<int:id>/',
        cambiar_estado_cajero,
        name='cambiar_estado_cajero'
    ),

    # Eliminar cajero
    path(
        'cajeros/eliminar/<int:id>/',
        eliminar_cajero,
        name='eliminar_cajero'
    ),

]