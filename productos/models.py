from django.db import models
from foodtrucks.models import FoodTruck


class Producto(models.Model):

    foodtruck = models.ForeignKey(
        FoodTruck,
        on_delete=models.CASCADE
    )

    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField()


    # Convertir los textos a mayúscula antes de guardar
    def save(self, *args, **kwargs):

        self.nombre = self.nombre.upper()

        super().save(*args, **kwargs)


    def __str__(self):
        return self.nombre