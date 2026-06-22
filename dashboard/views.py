from django.shortcuts import render
from django.utils import timezone
from decimal import Decimal
from usuarios.utils import obtener_empresa

from caja.models import MovimientoCaja
from pedidos.models import Pedido
from compras.models import Compra
from productos.models import Producto
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
  
    empresa = obtener_empresa(request)

    hoy = timezone.localdate()

    ventas_hoy = (
        MovimientoCaja.objects.filter(
            tipo="ingreso",
            empresa=empresa,
            creado__date=hoy
        )
    )

    total_ventas = sum(
        movimiento.monto
        for movimiento in ventas_hoy
    )

    pedidos_pendientes = Pedido.objects.filter(
        empresa=empresa,
        estado="pendiente"
    ).count()

    compras_hoy = Compra.objects.filter(
        empresa=empresa,
        creado__date=hoy
    ).count()

    stock_critico = sum(
    1
    for producto in Producto.objects.filter(
        empresa=empresa
    )
    if producto.stock <= producto.stock_minimo
)

    context = {
        "total_ventas": total_ventas or Decimal("0"),
        "pedidos_pendientes": pedidos_pendientes,
        "compras_hoy": compras_hoy,
        "stock_critico": stock_critico,
        "empresa": empresa,
    }

    return render(
        request,
        "dashboard/inicio.html",
        context,
    )