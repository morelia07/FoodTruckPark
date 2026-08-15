from django.contrib import admin
from django.urls import path, include
from .views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', dashboard, name='dashboard'),

    path('usuarios/', include('usuarios.urls')),

    path('foodtrucks/', include('foodtrucks.urls')),

    path('productos/', include('productos.urls')),

    path('ventas/', include('ventas.urls')),

    path('reportes/', include('reportes.urls')),
]