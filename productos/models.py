from django.db import models
from empresas.models import Empresa
from categorias.models import Categoria
from django.core.exceptions import ValidationError

class Producto(models.Model):
    empresa = models.ForeignKey(
    Empresa,
    on_delete=models.CASCADE,
    related_name="productos"
    )

    categoria = models.ForeignKey(
    Categoria,
    on_delete=models.PROTECT,
    related_name="productos"
    )

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    imagen = models.ImageField(
        upload_to="productos/",
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    stock_minimo = models.PositiveIntegerField(
        default=0
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
        
    def clean(self):
      if self.categoria_id and self.empresa_id:
          if self.categoria.empresa != self.empresa:
              raise ValidationError(
                  "La categoría debe pertenecer a la misma empresa que el producto."
              )

    def __str__(self):
      return f"{self.nombre} ({self.empresa.nombre})"