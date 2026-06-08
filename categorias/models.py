from django.db import models
from empresas.models import Empresa


class Categoria(models.Model):
  
    empresa = models.ForeignKey(
    Empresa,
    on_delete=models.CASCADE,
    related_name="categorias"
    )

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    icono = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    orden = models.PositiveIntegerField(
        default=0
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"