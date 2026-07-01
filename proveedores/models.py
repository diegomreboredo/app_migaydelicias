from django.db import models

from empresas.models import Empresa


class Proveedor(models.Model):

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="proveedores"
    )

    nombre = models.CharField(
        max_length=100
    )

    razon_social = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    cuit = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    
    contacto = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    telefono = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    direccion = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    
    ciudad = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    
    provincia = models.CharField(
        max_length=100,
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
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"