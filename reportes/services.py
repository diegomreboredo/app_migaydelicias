from django.db.models import Sum, Avg, Count
from django.utils import timezone

from pedidos.models import Pedido, DetallePedido

def obtener_metricas(empresa):

    metricas = {}

    hoy = timezone.localdate()

    ahora = timezone.now()

    # Ventas de hoy
    metricas["ventas_hoy"] = (
        Pedido.objects.filter(
            empresa=empresa,
            estado_pago="pagado",
            creado__date=hoy
        ).aggregate(
            total=Sum("total")
        )["total"] or 0
    )

    # Ventas del mes
    metricas["ventas_mes"] = (
        Pedido.objects.filter(
            empresa=empresa,
            estado_pago="pagado",
            creado__year=ahora.year,
            creado__month=ahora.month
        ).aggregate(
            total=Sum("total")
        )["total"] or 0
    )

    # Pedidos
    metricas["cantidad_pedidos"] = Pedido.objects.filter(
        empresa=empresa
    ).count()

    # Ticket promedio
    metricas["ticket_promedio"] = (
        Pedido.objects.filter(
            empresa=empresa,
            estado_pago="pagado"
        ).aggregate(
            promedio=Avg("total")
        )["promedio"] or 0
    )
    
    # Cobrado en efectivo
    metricas["efectivo"] = (
        Pedido.objects.filter(
            empresa=empresa,
            estado_pago="pagado",
            forma_pago="efectivo"
        ).aggregate(
            total=Sum("total")
        )["total"] or 0
    )
    
    # Cobrado por transferencia
    metricas["transferencia"] = (
        Pedido.objects.filter(
            empresa=empresa,
            estado_pago="pagado",
            forma_pago="transferencia"
        ).aggregate(
            total=Sum("total")
        )["total"] or 0
    )
    
    producto = (
        DetallePedido.objects.filter(
            pedido__empresa=empresa
        )
        .values("producto__nombre")
        .annotate(
            vendidos=Sum("cantidad")
        )
        .order_by("-vendidos")
        .first()
    )
    
    metricas["producto_top"] = producto
    
    cliente = (
        Pedido.objects.filter(
            empresa=empresa
        )
        .values("cliente__nombre")
        .annotate(
            pedidos=Count("id"),
            total=Sum("total")
        )
        .order_by("-total")
        .first()
    )
    
    metricas["cliente_top"] = cliente

    return metricas