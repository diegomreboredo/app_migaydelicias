from django.db.models import Sum, Avg, Count
from django.utils import timezone

from pedidos.models import Pedido, DetallePedido
from datetime import timedelta
from django.db.models.functions import TruncDate

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
    
    
    hace_30_dias = hoy - timedelta(days=29)
    ventas_db = (
        Pedido.objects.filter(
            empresa=empresa,
            estado_pago="pagado",
            creado__date__gte=hace_30_dias
        )
        .annotate(
            dia=TruncDate("creado")
        )
        .values("dia")
        .annotate(
            ventas=Sum("total")
        )
    )
    
    ventas_dict = {
        venta["dia"]: float(venta["ventas"])
        for venta in ventas_db
    }
    
    ventas_30_dias = []
    
    for i in range(30):
    
        fecha = hace_30_dias + timedelta(days=i)
    
        ventas_30_dias.append({
    
            "dia": fecha.strftime("%d/%m"),
    
            "ventas": ventas_dict.get(
                fecha,
                0
            )
    
        })
    
    metricas["ventas_30_dias"] = ventas_30_dias
    
    metricas["formas_pago"] = [
        {
            "forma": "Efectivo",
            "monto": float(metricas["efectivo"]),
        },
        {
            "forma": "Transferencia",
            "monto": float(metricas["transferencia"]),
        },
    ]
    
    top_productos = (
        DetallePedido.objects.filter(
            pedido__empresa=empresa
        )
        .values("producto__nombre")
        .annotate(
            vendidos=Sum("cantidad")
        )
        .order_by("-vendidos")[:10]
    )
    
    metricas["top_productos"] = list(top_productos)
    
    top_clientes = (
        Pedido.objects.filter(
            empresa=empresa
        )
        .values("cliente__nombre")
        .annotate(
            total=Sum("total")
        )
        .order_by("-total")[:10]
    )
    
    metricas["top_clientes"] = list(top_clientes)

    return metricas