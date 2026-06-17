from django.db import models
from django.core.exceptions import ValidationError
from empresas.models import Empresa
from clientes.models import Cliente
from productos.models import Producto
from django.db.models import Sum
from inventario.models import MovimientoInventario
from caja.models import MovimientoCaja


class Pedido(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("preparacion", "En preparación"),
        ("listo", "Listo"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="pedidos"
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
    
    stock_descontado = models.BooleanField(
    default=False
    )
    
    caja_registrada = models.BooleanField(
        default=False
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    actualizado = models.DateTimeField(
        auto_now=True
    )
    
    def clean(self):
      if self.cliente.empresa != self.empresa:
          raise ValidationError(
              "El cliente debe pertenecer a la misma empresa del pedido."
          )

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
      return (
          f"Pedido #{self.id} - "
          f"{self.empresa.nombre} - "
          f"{self.cliente.nombre}"
      )
      
    def save(self, *args, **kwargs):
      
          es_nuevo = self.pk is None
      
          estado_anterior = None
      
          if not es_nuevo:
              estado_anterior = Pedido.objects.get(
                  pk=self.pk
              ).estado
      
          super().save(*args, **kwargs)
      
          if (
              not es_nuevo
              and estado_anterior != "entregado"
              and self.estado == "entregado"
              and not self.stock_descontado
          ):
              self.descontar_stock()
    
    def descontar_stock(self):

      if self.stock_descontado:
          return
  
      for detalle in self.detalles.all():
  
          MovimientoInventario.objects.create(
              empresa=self.empresa,
              producto=detalle.producto,
              tipo="venta",
              cantidad=detalle.cantidad,
              motivo="Salida por venta",
              referencia=f"Pedido #{self.id}",
          )
  
      self.stock_descontado = True
  
      self.save(
          update_fields=["stock_descontado"]
      )
      
      self.registrar_ingreso_caja()
    
    def registrar_ingreso_caja(self):

        if self.caja_registrada:
            return
    
        MovimientoCaja.objects.create(
          empresa=self.empresa,
          tipo="ingreso",
          concepto="Venta de productos",
          referencia=f"Pedido #{self.id}",
          monto=self.total,
          observaciones=f"Cliente: {self.cliente.nombre}"
      )
    
        self.caja_registrada = True
    
        self.save(
            update_fields=["caja_registrada"]
        )
        
class DetallePedido(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="detalles_pedido"
    )

    cantidad = models.PositiveIntegerField(
        default=1
    )

    precio_unitario = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      blank=True,
      null=True
    )

    subtotal = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      default=0,
      blank=True,
      null=True
    )
    
    def clean(self):
      if self.producto.empresa != self.pedido.empresa:
          raise ValidationError(
              "El producto debe pertenecer a la misma empresa del pedido."
          )
      if self.cantidad > self.producto.stock:
        raise ValidationError(
            f"Stock insuficiente. Disponible: {self.producto.stock}"
        )
          
    def save(self, *args, **kwargs):
      self.precio_unitario = self.producto.precio
      self.subtotal = self.cantidad * self.precio_unitario
  
      super().save(*args, **kwargs)
  
      total = self.pedido.detalles.aggregate(
          total=Sum("subtotal")
      )["total"] or 0
  
      self.pedido.total = total
      self.pedido.save()

    class Meta:
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedido"

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"