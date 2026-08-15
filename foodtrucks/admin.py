from django.contrib import admin
from .models import FoodTruck


@admin.register(FoodTruck)
class FoodTruckAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'propietario',
        'tipo_comida',
        'estado'
    )