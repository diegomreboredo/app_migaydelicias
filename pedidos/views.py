from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import PedidoForm
from .models import Pedido, DetallePedido
from django.shortcuts import get_object_or_404
from .forms_detalle import DetallePedidoForm
from productos.models import Producto
from categorias.models import Categoria
from django.contrib import messages

@login_required
def lista_pedidos(request):

    empresa = request.user.empresa_usuario.empresa

    q = request.GET.get("q")

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

    cancelados = Pedido.objects.filter(
        empresa=empresa,
        estado="cancelado"
    )

    if q:

        pendientes = pendientes.filter(
            cliente__nombre__icontains=q
        )

        preparacion = preparacion.filter(
            cliente__nombre__icontains=q
        )

        listos = listos.filter(
            cliente__nombre__icontains=q
        )

        entregados = entregados.filter(
            cliente__nombre__icontains=q
        )

        cancelados = cancelados.filter(
            cliente__nombre__icontains=q
        )

    pedidos_hoy = Pedido.objects.filter(
        empresa=empresa
    ).count()

    pendientes_total = pendientes.count()

    preparacion_total = preparacion.count()

    listos_total = listos.count()

    cancelados_total = cancelados.count()

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
        "cancelados": cancelados,
        "cancelados_total": cancelados_total,
        "pedidos_hoy": pedidos_hoy,
        "pendientes_total": pendientes_total,
        "preparacion_total": preparacion_total,
        "listos_total": listos_total,
        "facturacion_total": facturacion_total,
        "q": q,
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
        
        return redirect(
            "detalle_pedido",
            pedido_id=pedido.id
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
    
    total_unidades = sum(
    detalle.cantidad
    for detalle in pedido.detalles.all()
)
    total_unidades = sum(
    detalle.cantidad
    for detalle in pedido.detalles.all()
)

    return render(
        request,
        "pedidos/detalle.html",
        {
            "pedido": pedido,
            "empresa": empresa,
            "total_unidades": total_unidades,
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

    estado_anterior = pedido.estado

    if (
        nuevo_estado == "cancelado"
        and estado_anterior != "cancelado"
    ):

        for detalle in pedido.detalles.all():

            producto = detalle.producto

            producto.stock_reservado -= detalle.cantidad

            if producto.stock_reservado < 0:
                producto.stock_reservado = 0

            producto.save(
                update_fields=["stock_reservado"]
            )

    pedido.estado = nuevo_estado

    pedido.save()

    return redirect(
        "detalle_pedido",
        pedido_id=pedido.id
    )
    
@login_required
def agregar_producto_pedido(request, pedido_id):

    empresa = request.user.empresa_usuario.empresa

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        empresa=empresa
    )
    
    q = request.GET.get("q", "")
    categoria_id = request.GET.get("categoria")
    
    productos = Producto.objects.filter(
        empresa=empresa,
        activo=True
    )
    
    if q:
        productos = productos.filter(
            nombre__icontains=q
        )
    
    if categoria_id:
        productos = productos.filter(
            categoria_id=categoria_id
        )
    
    categorias = Categoria.objects.filter(
        empresa=empresa,
        activo=True
    )

    if request.method == "POST":

        form = DetallePedidoForm(
            empresa,
            request.POST
        )

        if form.is_valid():

            producto = form.cleaned_data["producto"]
            cantidad = form.cleaned_data["cantidad"]
            
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
            )
            print("RESERVANDO:", producto.nombre, cantidad)
            producto.stock_reservado += cantidad
            producto.save(
                update_fields=["stock_reservado"]
            )
            print("RESERVADO:", producto.stock_reservado)

            return redirect(
                "detalle_pedido",
                pedido_id=pedido.id
            )

    else:

        form = DetallePedidoForm(
            empresa
        )

    return render(
        request,
        "pedidos/agregar_producto.html",
        {
            "pedido": pedido,
            "form": form,
            "empresa": empresa,
            "productos": productos,
            "categorias": categorias,
            "q": q,
            "categoria_id": categoria_id,
        }
    )
    
@login_required
def eliminar_detalle_pedido(request, detalle_id):

    empresa = request.user.empresa_usuario.empresa

    detalle = get_object_or_404(
        DetallePedido,
        id=detalle_id,
        pedido__empresa=empresa
    )

    pedido = detalle.pedido
    
    producto = detalle.producto

    producto.stock_reservado -= detalle.cantidad
    
    if producto.stock_reservado < 0:
        producto.stock_reservado = 0
    
    producto.save(
        update_fields=["stock_reservado"]
    )

    detalle.delete()

    total = sum(
        d.subtotal
        for d in pedido.detalles.all()
    )

    pedido.total = total

    pedido.save(
        update_fields=["total"]
    )

    return redirect(
        "detalle_pedido",
        pedido_id=pedido.id
    )
    
@login_required
def sumar_cantidad_detalle(request, detalle_id):

    empresa = request.user.empresa_usuario.empresa

    detalle = get_object_or_404(
        DetallePedido,
        id=detalle_id,
        pedido__empresa=empresa
    )

    if detalle.producto.stock_disponible > 0:

        detalle.cantidad += 1

        detalle.producto.stock_reservado += 1
        detalle.producto.save(
            update_fields=["stock_reservado"]
        )

        detalle.save()

        messages.success(
            request,
            "Se agregó una unidad."
        )

    else:

        messages.error(
            request,
            "No hay stock disponible para agregar otra unidad."
        )

    return redirect(
        "detalle_pedido",
        pedido_id=detalle.pedido.id
    )
    
@login_required
def restar_cantidad_detalle(request, detalle_id):

    empresa = request.user.empresa_usuario.empresa

    detalle = get_object_or_404(
        DetallePedido,
        id=detalle_id,
        pedido__empresa=empresa
    )

    if detalle.cantidad > 1:

        detalle.cantidad -= 1

        if detalle.producto.stock_reservado > 0:
            detalle.producto.stock_reservado -= 1
            detalle.producto.save(
                update_fields=["stock_reservado"]
            )

        detalle.save()

        messages.success(
            request,
            "Se quitó una unidad."
        )

    else:

        messages.warning(
            request,
            "La cantidad mínima es 1."
        )

    return redirect(
        "detalle_pedido",
        pedido_id=detalle.pedido.id
    )
    