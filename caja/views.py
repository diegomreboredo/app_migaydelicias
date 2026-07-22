from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MovimientoCajaForm, AperturaCajaForm, CierreCajaForm
from django.shortcuts import redirect
from pedidos.models import Pedido
from django.utils import timezone
from .models import Caja, MovimientoCaja
from django.shortcuts import get_object_or_404

def obtener_caja_abierta(empresa):

    return Caja.objects.filter(
        empresa=empresa,
        abierta=True
    ).first()


@login_required
def lista_caja(request):

    empresa = request.user.empresa_usuario.empresa
    
    caja_abierta = obtener_caja_abierta(empresa)
    
    if not caja_abierta:
        return redirect("abrir_caja")

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
    
    caja_abierta = obtener_caja_abierta(empresa)

    if not caja_abierta:
        return redirect("abrir_caja")

    if request.method == "POST":

        form = MovimientoCajaForm(request.POST)

        if form.is_valid():

            movimiento = form.save(commit=False)

            movimiento.empresa = empresa
            
            caja_abierta = obtener_caja_abierta(empresa)
            
            if not caja_abierta:
                return redirect("abrir_caja")
            
            movimiento.caja = caja_abierta
            
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
    
    caja_abierta = obtener_caja_abierta(empresa)

    if not caja_abierta:
        return redirect("abrir_caja")

    movimientos = caja_abierta.movimientos.all()

    ingresos = sum(
        m.monto for m in movimientos
        if m.tipo == "ingreso"
    )

    egresos = sum(
        m.monto for m in movimientos
        if m.tipo == "egreso"
    )

    saldo_actual = (
        caja_abierta.saldo_inicial +
        ingresos -
        egresos
    )
    actividad_reciente = (
        movimientos
        .order_by("-creado")[:8]
    )
    
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
        "ingresos": ingresos,
        "egresos": egresos,
        "ultimos_pedidos": ultimos_pedidos,
        "pedidos_pendientes": pedidos_pendientes,
        "ventas_hoy": ventas_hoy,
        "pedidos_entregados_hoy": pedidos_entregados_hoy,
        "caja_abierta": caja_abierta,
        "saldo_actual": saldo_actual,
        "actividad_reciente": actividad_reciente,
        
    }

    return render(
        request,
        "caja/inicio.html",
        context
    )
    
@login_required
def abrir_caja(request):

    empresa = request.user.empresa_usuario.empresa

    if request.method == "POST":

        form = AperturaCajaForm(request.POST)

        if form.is_valid():

            caja = form.save(commit=False)

            caja.empresa = empresa
            caja.usuario_apertura = request.user

            caja.save()

            return redirect("inicio_caja")

    else:

        form = AperturaCajaForm()

    return render(
        request,
        "caja/abrir.html",
        {
            "form": form,
            "empresa": empresa,
        }
    )
    
@login_required
def cerrar_caja(request):

    empresa = request.user.empresa_usuario.empresa
    
    caja = obtener_caja_abierta(empresa)

    if not caja:
        return redirect("abrir_caja")
        
    movimientos = caja.movimientos.all()

    ingresos = sum(
        m.monto
        for m in movimientos
        if m.tipo == "ingreso"
    )
    
    egresos = sum(
        m.monto
        for m in movimientos
        if m.tipo == "egreso"
    )
    
    saldo_esperado = (
        caja.saldo_inicial +
        ingresos -
        egresos
    )

    if request.method == "POST":

        form = CierreCajaForm(
            request.POST,
            instance=caja
        )
    
        if form.is_valid():
    
            caja = form.save(commit=False)
    
            diferencia = caja.saldo_contado - saldo_esperado
    
            if (
                diferencia != 0
                and not caja.observaciones_cierre
            ):
    
                form.add_error(
                    "observaciones_cierre",
                    "Debe ingresar una observación cuando existe una diferencia en el arqueo."
                )
    
            else:
    
                caja.abierta = False
                caja.fecha_cierre = timezone.now()
                caja.usuario_cierre = request.user
    
                caja.save()
    
                return redirect("inicio_caja")
    
    else:
    
        form = CierreCajaForm(instance=caja)
    
    return render(
        request,
        "caja/cerrar.html",
        {
            "form": form,
            "empresa": empresa,
            "caja": caja,
            "saldo_esperado": saldo_esperado,
            "ingresos": ingresos,
            "egresos": egresos,
        }
    )
    
@login_required
def historial_cajas(request):

    empresa = request.user.empresa_usuario.empresa

    cajas = (
        Caja.objects
        .filter(empresa=empresa)
        .order_by("-fecha_apertura")
    )

    return render(
        request,
        "caja/historial.html",
        {
            "empresa": empresa,
            "cajas": cajas,
        }
    )
    


@login_required
def detalle_caja(request, pk):

    empresa = request.user.empresa_usuario.empresa

    caja = get_object_or_404(
        Caja,
        pk=pk,
        empresa=empresa
    )

    movimientos = caja.movimientos.all().order_by("creado")

    ingresos = sum(
        m.monto
        for m in movimientos
        if m.tipo == "ingreso"
    )

    egresos = sum(
        m.monto
        for m in movimientos
        if m.tipo == "egreso"
    )

    saldo_esperado = (
        caja.saldo_inicial +
        ingresos -
        egresos
    )

    diferencia = None

    if caja.saldo_contado is not None:
        diferencia = caja.saldo_contado - saldo_esperado

    return render(
        request,
        "caja/detalle.html",
        {
            "empresa": empresa,
            "caja": caja,
            "movimientos": movimientos,
            "ingresos": ingresos,
            "egresos": egresos,
            "saldo_esperado": saldo_esperado,
            "diferencia": diferencia,
        }
    )