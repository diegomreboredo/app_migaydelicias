from django.db import models

from empresas.models import Empresa


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