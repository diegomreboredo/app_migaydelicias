from django.db import models

from empresas.models import Empresa
from proveedores.models import Proveedor


class Compra(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("recibida", "Recibida"),
        ("cancelada", "Cancelada"),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="compras"
    )

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="compras"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    stock_ingresado = models.BooleanField(
      default=False
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    actualizado = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return (
            f"Compra #{self.id} - "
            f"{self.empresa.nombre} - "
            f"{self.proveedor.nombre}"
        )
        
    def save(self, *args, **kwargs):

      es_nueva = self.pk is None
  
      estado_anterior = None
  
      if not es_nueva:
          estado_anterior = Compra.objects.get(
              pk=self.pk
          ).estado
  
      super().save(*args, **kwargs)
  
      if (
          not es_nueva
          and estado_anterior != "recibida"
          and self.estado == "recibida"
          and not self.stock_ingresado
      ):
          self.ingresar_stock()
      
    def ingresar_stock(self):

      if self.stock_ingresado:
          return
  
      print("=== INGRESANDO STOCK ===")
  
      for detalle in self.detalles.all():
  
          print(
              detalle.producto.nombre,
              detalle.cantidad
          )
        
from productos.models import Producto


class DetalleCompra(models.Model):

    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="detalles_compra"
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de Compra"

    def __str__(self):
        return (
            f"{self.producto.nombre} "
            f"x {self.cantidad}"
        )
        
    def save(self, *args, **kwargs):

      self.subtotal = (
          self.cantidad *
          self.precio_unitario
      )
  
      super().save(*args, **kwargs)
  
      compra = self.compra
  
      compra.total = sum(
          detalle.subtotal
          for detalle in compra.detalles.all()
      )
  
      compra.save(
          update_fields=["total"]
      )