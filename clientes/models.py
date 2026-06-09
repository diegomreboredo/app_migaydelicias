from django.db import models
from empresas.models import Empresa


class Cliente(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="clientes"
    )

    nombre = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    direccion = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    actualizado = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
      return f"{self.empresa.nombre} - {self.nombre}"