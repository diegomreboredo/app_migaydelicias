from django.db import models
from django.conf import settings
from empresas.models import Empresa


class Caja(models.Model):

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="cajas"
    )

    abierta = models.BooleanField(
        default=True
    )

    saldo_inicial = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    fecha_apertura = models.DateTimeField(
        auto_now_add=True
    )

    fecha_cierre = models.DateTimeField(
        blank=True,
        null=True
    )
    
    saldo_contado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )
    
    observaciones_cierre = models.TextField(
        blank=True,
        null=True
    )

    usuario_apertura = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="cajas_abiertas"
    )

    usuario_cierre = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="cajas_cerradas",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-fecha_apertura"]

    def __str__(self):
        estado = "Abierta" if self.abierta else "Cerrada"
        return f"Caja {self.fecha_apertura:%d/%m/%Y} - {estado}"
class MovimientoCaja(models.Model):

    TIPOS = [
        ("ingreso", "Ingreso"),
        ("egreso", "Egreso"),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="movimientos_caja"
    )
    
    caja = models.ForeignKey(
        Caja,
        on_delete=models.PROTECT,
        related_name="movimientos",
        null=True,
        blank=True
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    concepto = models.CharField(
        max_length=200
    )
    
    referencia = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Movimiento de Caja"
        verbose_name_plural = "Movimientos de Caja"

    def __str__(self):
        return (
            f"{self.get_tipo_display()} - "
            f"{self.concepto} - "
            f"${self.monto}"
        )