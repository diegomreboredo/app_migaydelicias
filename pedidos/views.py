from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import PedidoForm
from .models import Pedido, DetallePedido
from django.shortcuts import get_object_or_404

@login_required
def lista_pedidos(request):

    empresa = request.user.empresa_usuario.empresa
    
    pendientes = Pedido.objects.filter(
        empresa=empresa,
        estado="pendiente"
    )
    
    preparacion = Pedido.objects.filter(
        empresa=empresa,
        estado="preparacion"
    )
    
    listos = Pedido.objects.filter(
        empresa=empresa,
        estado="listo"
    )
    
    entregados = Pedido.objects.filter(
        empresa=empresa,
        estado="entregado"
    )
    
    pedidos_hoy = Pedido.objects.filter(
        empresa=empresa
    ).count()
    
    pendientes_total = pendientes.count()
    
    preparacion_total = preparacion.count()
    
    listos_total = listos.count()
    
    facturacion_total = sum(
        pedido.total
        for pedido in entregados
    )
    
    context = {
        "empresa": empresa,
        "pendientes": pendientes,
        "preparacion": preparacion,
        "listos": listos,
        "entregados": entregados,
        "pedidos_hoy": pedidos_hoy,
        "pendientes_total": pendientes_total,
        "preparacion_total": preparacion_total,
        "listos_total": listos_total,
        "facturacion_total": facturacion_total,
    }
    
    return render(
        request,
        "pedidos/lista.html",
        context
    )

@login_required
def nuevo_pedido(request):

    empresa = request.user.empresa_usuario.empresa
    
    if request.method == "POST":
    
        form = PedidoForm(
            empresa,
            request.POST
        )
    
        if form.is_valid():
    
            pedido = Pedido.objects.create(
                empresa=empresa,
                cliente=form.cleaned_data["cliente"],
                observaciones=form.cleaned_data["observaciones"],
            )
    
            DetallePedido.objects.create(
                pedido=pedido,
                producto=form.cleaned_data["producto"],
                cantidad=form.cleaned_data["cantidad"],
            )
    
            return redirect(
                "lista_pedidos"
            )
    
    else:
    
        form = PedidoForm(
            empresa
        )
    
    return render(
        request,
        "pedidos/nuevo.html",
        {
            "form": form,
            "empresa": empresa,
        }
    )
@login_required
def detalle_pedido(request, pedido_id):

    empresa = request.user.empresa_usuario.empresa

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        empresa=empresa
    )

    return render(
        request,
        "pedidos/detalle.html",
        {
            "pedido": pedido,
            "empresa": empresa,
        }
    )
    
@login_required
def cambiar_estado(request, pedido_id, nuevo_estado):

    empresa = request.user.empresa_usuario.empresa

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        empresa=empresa
    )

    pedido.estado = nuevo_estado

    pedido.save()

    return redirect(
        "detalle_pedido",
        pedido_id=pedido.id
    )