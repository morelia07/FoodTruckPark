from django.urls import path
from . import views


urlpatterns = [

    # Lista de ventas
    path('', views.lista_ventas, name='lista_ventas'),

    # Crear venta
    path('nuevo/', views.crear_venta, name='crear_venta'),
    
    path('detalle/<int:id>/', views.detalle_venta, name='detalle_venta'),

]