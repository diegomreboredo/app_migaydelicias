from django.shortcuts import render
from django.utils import timezone
from decimal import Decimal

from caja.models import MovimientoCaja
from pedidos.models import Pedido
from compras.models import Compra
from productos.models import Producto


def inicio(request):

    hoy = timezone.localdate()

    ventas_hoy = (
        MovimientoCaja.objects.filter(
            tipo="ingreso",
            creado__date=hoy
        )
    )

    total_ventas = sum(
        movimiento.monto
        for movimiento in ventas_hoy
    )

    pedidos_pendientes = Pedido.objects.filter(
        estado="pendiente"
    ).count()

    compras_hoy = Compra.objects.filter(
        creado__date=hoy
    ).count()

    stock_critico = Producto.objects.filter(
        stock__lte=5
    ).count()

    context = {
        "total_ventas": total_ventas or Decimal("0"),
        "pedidos_pendientes": pedidos_pendientes,
        "compras_hoy": compras_hoy,
        "stock_critico": stock_critico,
    }

    return render(
        request,
        "dashboard/inicio.html",
        context,
    )