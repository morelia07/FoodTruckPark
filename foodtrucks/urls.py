from django.urls import path
from . import views

urlpatterns = [
    # Lista de Food Trucks
    path('', views.lista_foodtrucks, name='lista_foodtrucks'),

    # Registrar un nuevo Food Truck
    path('nuevo/', views.crear_foodtruck, name='crear_foodtruck'),

    # Editar un Food Truck
    path('editar/<int:id>/', views.editar_foodtruck, name='editar_foodtruck'),

    # Eliminar un Food Truck
    path('eliminar/<int:id>/', views.eliminar_foodtruck, name='eliminar_foodtruck'),
]