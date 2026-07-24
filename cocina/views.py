from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from pedidos.models import Pedido
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def panel_cocina(request):

    empresa = request.user.empresa_usuario.empresa

    pedidos_pendientes = Pedido.objects.filter(
        empresa=empresa,
        estado="pendiente"
    ).prefetch_related("detalles__producto")

    pedidos_preparacion = Pedido.objects.filter(
        empresa=empresa,
        estado="preparacion"
    ).prefetch_related("detalles__producto")

    pedidos_listos = Pedido.objects.filter(
        empresa=empresa,
        estado="listo"
    ).prefetch_related("detalles__producto")

    return render(
        request,
        "cocina/panel.html",
        {
            "pedidos_pendientes": pedidos_pendientes,
            "pedidos_preparacion": pedidos_preparacion,
            "pedidos_listos": pedidos_listos,
        }
    )
    
@login_required
def actualizar_panel(request):

    empresa = request.user.empresa_usuario.empresa

    pedidos_pendientes = Pedido.objects.filter(
        empresa=empresa,
        estado="pendiente"
    ).prefetch_related("detalles__producto")

    pedidos_preparacion = Pedido.objects.filter(
        empresa=empresa,
        estado="preparacion"
    ).prefetch_related("detalles__producto")

    pedidos_listos = Pedido.objects.filter(
        empresa=empresa,
        estado="listo"
    ).prefetch_related("detalles__producto")

    html = render_to_string(
        "cocina/partials/columnas.html",
        {
            "pedidos_pendientes": pedidos_pendientes,
            "pedidos_preparacion": pedidos_preparacion,
            "pedidos_listos": pedidos_listos,
        },
        request=request,
    )

    return JsonResponse({
        "html": html
    })