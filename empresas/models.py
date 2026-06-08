from django.db import models


class Empresa(models.Model):
    nombre = models.CharField(
        max_length=150
    )

    razon_social = models.CharField(
        max_length=200,
        blank=True
    )

    cuit = models.CharField(
        max_length=20,
        blank=True
    )

    telefono = models.CharField(
        max_length=50,
        blank=True
    )

    direccion = models.TextField(
        blank=True
    )

    activa = models.BooleanField(
        default=True
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre