from django.urls import path
from . import views


urlpatterns = [

    # Lista de productos
    path('', views.lista_productos, name='lista_productos'),

    # Crear producto
    path('nuevo/', views.crear_producto, name='crear_producto'),

    # Editar producto
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),

    # Eliminar producto
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

]