from django.db import models


class FoodTruck(models.Model):

    nombre = models.CharField(max_length=100)
    propietario = models.CharField(max_length=100)
    tipo_comida = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)


    # Convertir los textos a mayúscula antes de guardar
    def save(self, *args, **kwargs):

        self.nombre = self.nombre.upper()
        self.propietario = self.propietario.upper()
        self.tipo_comida = self.tipo_comida.upper()

        super().save(*args, **kwargs)


    def __str__(self):
        return self.nombre