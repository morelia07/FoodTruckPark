from django.db import models
from django.contrib.auth.models import User

from foodtrucks.models import FoodTruck
from productos.models import Producto


class Venta(models.Model):

    METODOS_PAGO = [
        ('EFECTIVO', 'EFECTIVO'),
        ('TARJETA', 'TARJETA'),
        ('TRANSFERENCIA', 'TRANSFERENCIA'),
    ]

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    metodo_pago = models.CharField(
        max_length=20,
        choices=METODOS_PAGO
    )

    numero_autorizacion = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    cajero = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):

        return f"Factura #{self.id}"


class DetalleVenta(models.Model):

    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE
    )

    foodtruck = models.ForeignKey(
        FoodTruck,
        on_delete=models.CASCADE
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    cantidad = models.PositiveIntegerField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):

        return self.cantidad * self.precio

    def __str__(self):

        return f"{self.producto.nombre} - {self.cantidad}"