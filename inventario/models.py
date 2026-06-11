from django.db import models, transaction
from django.core.exceptions import ValidationError

from empresas.models import Empresa
from productos.models import Producto


class MovimientoInventario(models.Model):

    TIPOS = [
        ("ingreso", "Ingreso"),
        ("salida", "Salida"),
        ("ajuste", "Ajuste"),
        ("compra", "Compra"),
        ("venta", "Venta"),
        ("merma", "Merma"),
        ("devolucion", "Devolución"),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="movimientos_inventario"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="movimientos_inventario"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    cantidad = models.PositiveIntegerField()

    motivo = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    
    referencia = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"

    def __str__(self):
        return (
            f"{self.producto.nombre} - "
            f"{self.get_tipo_display()} "
            f"({self.cantidad})"
        )
        
    def clean(self):

      if self.tipo in ("salida", "venta", "merma"):
  
          if self.cantidad > self.producto.stock:
  
              raise ValidationError(
                  f"Stock insuficiente. Disponible: {self.producto.stock}"
              )
    
    def save(self, *args, **kwargs):

        es_nuevo = self.pk is None
        
        self.full_clean()

        with transaction.atomic():

            super().save(*args, **kwargs)

            if not es_nuevo:

                return

            if self.tipo in ("ingreso", "compra", "devolucion"):

                self.producto.stock += self.cantidad

            elif self.tipo in ("salida", "venta", "merma"):

                self.producto.stock -= self.cantidad

            self.producto.save(
                update_fields=["stock"]
            )