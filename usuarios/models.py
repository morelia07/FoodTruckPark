
from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):

    ROLES = [
        ('ADMIN', 'Administrador'),
        ('CAJERO', 'Cajero'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    rol = models.CharField(
        max_length=10,
        choices=ROLES,
        default='CAJERO'
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"

