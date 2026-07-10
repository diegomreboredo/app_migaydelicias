from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import MovimientoCaja
from .forms import MovimientoCajaForm
from django.shortcuts import redirect
from pedidos.models import Pedido
from django.utils import timezone


@login_required
def lista_caja(request):

    empresa = request.user.empresa_usuario.empresa

    q = request.GET.get("q", "")
    tipo = request.GET.get("tipo", "")
    fecha_desde = request.GET.get("desde", "")
    fecha_hasta = request.GET.get("hasta", "")

    # Todos los movimientos (para las métricas)
    movimientos_empresa = MovimientoCaja.objects.filter(
        empresa=empresa
    )

    # Movimientos filtrados (para la tabla)
    movimientos = movimientos_empresa

    if q:

        movimientos = movimientos.filter(
            concepto__icontains=q
        )

    if tipo:

        movimientos = movimientos.filter(
            tipo=tipo
        )
        
    if fecha_desde:

      movimientos = movimientos.filter(
          creado__date__gte=fecha_desde
      )

    if fecha_hasta:
    
        movimientos = movimientos.filter(
            creado__date__lte=fecha_hasta
        )

    ingresos = sum(
        m.monto
        for m in movimientos_empresa
        if m.tipo == "ingreso"
    )

    egresos = sum(
        m.monto
        for m in movimientos_empresa
        if m.tipo == "egreso"
    )

    saldo = ingresos - egresos
    saldo = round(saldo, 2)
    

    context = {
        "empresa": empresa,
        "movimientos": movimientos,
        "ingresos": ingresos,
        "egresos": egresos,
        "saldo": saldo,
        "q": q,
        "tipo": tipo,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
    }

    return render(
        request,
        "caja/lista.html",
        context
    )
    
@login_required
def nuevo_movimiento(request):

    empresa = request.user.empresa_usuario.empresa

    if request.method == "POST":

        form = MovimientoCajaForm(request.POST)

        if form.is_valid():

            movimiento = form.save(commit=False)

            movimiento.empresa = empresa

            movimiento.save()

            return redirect("lista_caja")

    else:

        form = MovimientoCajaForm()

    return render(
        request,
        "caja/nuevo.html",
        {
            "form": form,
            "empresa": empresa,
        }
    )
    
@login_required
def inicio_caja(request):

    empresa = request.user.empresa_usuario.empresa

    movimientos = MovimientoCaja.objects.filter(
        empresa=empresa
    )

    ingresos = sum(
        m.monto for m in movimientos
        if m.tipo == "ingreso"
    )

    egresos = sum(
        m.monto for m in movimientos
        if m.tipo == "egreso"
    )

    saldo = ingresos - egresos
    
    ultimos_pedidos = (
        Pedido.objects
        .filter(empresa=empresa)
        .order_by("-creado")[:5]
    )
    
    pedidos_pendientes = (
        Pedido.objects.filter(
            empresa=empresa,
            estado="pendiente"
        ).count()
    )
    
    ventas_hoy = Pedido.objects.filter(
        empresa=empresa,
        estado_pago="pagado",
        creado__date=timezone.localdate()
    ).count()
    
    pedidos_entregados_hoy = Pedido.objects.filter(
        empresa=empresa,
        estado="entregado",
        creado__date=timezone.localdate()
    ).count()

    context = {
        "empresa": empresa,
        "saldo": saldo,
        "ingresos": ingresos,
        "egresos": egresos,
        "ultimos_pedidos": ultimos_pedidos,
        "pedidos_pendientes": pedidos_pendientes,
        "ventas_hoy": ventas_hoy,
        "pedidos_entregados_hoy": pedidos_entregados_hoy,
    }

    return render(
        request,
        "caja/inicio.html",
        context
    )