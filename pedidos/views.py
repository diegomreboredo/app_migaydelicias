from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PedidoForm
from .models import Pedido, DetallePedido
from django.shortcuts import get_object_or_404
from .forms_detalle import DetallePedidoForm
from productos.models import Producto
from categorias.models import Categoria
from django.contrib import messages
from django.db.models import Sum
from .forms_pago import FormaPagoForm
from django.db.models import Max
from clientes.models import Cliente
from decimal import Decimal



@login_required
def lista_pedidos(request):

    empresa = request.user.empresa_usuario.empresa

    q = request.GET.get("q")
    estado = request.GET.get("estado", "todos")

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
    if estado != "todos":

      if estado != "pendiente":
          pendientes = pendientes.none()
  
      if estado != "preparacion":
          preparacion = preparacion.none()
  
      if estado != "listo":
          listos = listos.none()
  
      if estado != "entregado":
          entregados = entregados.none()
  
      if estado != "cancelado":
          cancelados = cancelados.none()

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
    
    pedidos_filtrados = Pedido.objects.none()

    if estado != "todos":
    
        pedidos_filtrados = Pedido.objects.filter(
            empresa=empresa,
            estado=estado
        )
    
        if q:
            pedidos_filtrados = pedidos_filtrados.filter(
                cliente__nombre__icontains=q
            )

    context = {
        "empresa": empresa,
        "pendientes": pendientes,
        "preparacion": preparacion,
        "listos": listos,
        "entregados": entregados,
        "cancelados": cancelados,
        "pedidos_filtrados": pedidos_filtrados,
        "cancelados_total": cancelados_total,
        "pedidos_hoy": pedidos_hoy,
        "pendientes_total": pendientes_total,
        "preparacion_total": preparacion_total,
        "listos_total": listos_total,
        "facturacion_total": facturacion_total,
        "q": q,
        "estado": estado,
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

            ultimo_numero = (
                Pedido.objects.filter(
                    empresa=empresa
                ).aggregate(
                    Max("numero")
                )["numero__max"]
            )
            
            pedido = Pedido(
                empresa=empresa,
                numero=(ultimo_numero or 0) + 1,
                cliente=form.cleaned_data["cliente"],
                observaciones=form.cleaned_data["observaciones"],
                
            )
            
            pedido.save()

            return redirect(
                "detalle_pedido",
                pedido_id=pedido.id
            )

    else:

        cliente_id = request.GET.get("cliente")

        form = PedidoForm(empresa)

        if cliente_id:
            form.initial["cliente"] = cliente_id

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
            producto.stock_reservado += cantidad
            producto.save(
                update_fields=["stock_reservado"]
            )

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
    
    if pedido.estado in ("entregado", "cancelado"):

      messages.error(
          request,
          "No se pueden eliminar productos de un pedido entregado o cancelado."
      )

      return redirect(
          "detalle_pedido",
          pedido_id=pedido.id
      )
    
    producto = detalle.producto

    producto.stock_reservado -= detalle.cantidad
    
    if producto.stock_reservado < 0:
        producto.stock_reservado = 0
    
    producto.save(
        update_fields=["stock_reservado"]
    )

    detalle.delete()

    pedido.total = (
    pedido.detalles.aggregate(
        total=Sum("subtotal")
    )["total"] or 0
)

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
    
@login_required
def marcar_pagado(request, pedido_id):

    empresa = request.user.empresa_usuario.empresa

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        empresa=empresa
    )

    if pedido.estado != "entregado":

        messages.error(
            request,
            "Solo se pueden cobrar pedidos entregados."
        )

        return redirect(
            "detalle_pedido",
            pedido_id=pedido.id
        )

    if pedido.estado_pago == "pagado":

        messages.warning(
            request,
            "Este pedido ya está pagado."
        )

        return redirect(
            "detalle_pedido",
            pedido_id=pedido.id
        )

    if request.method == "POST":

        form = FormaPagoForm(request.POST)

        if form.is_valid():

            pedido.forma_pago = form.cleaned_data["forma_pago"]
            pedido.estado_pago = "pagado"
            pedido.save(
                update_fields=["forma_pago", "estado_pago"]
            )

            if pedido.forma_pago == "efectivo":
                pedido.registrar_ingreso_caja()

            messages.success(
                request,
                "Pago registrado correctamente."
            )

            return redirect(
                "detalle_pedido",
                pedido_id=pedido.id
            )

    else:

        form = FormaPagoForm()

    return render(
        request,
        "pedidos/marcar_pagado.html",
        {
            "pedido": pedido,
            "form": form,
        }
    )
    
@login_required
def pos(request):

    empresa = request.user.empresa_usuario.empresa

    categorias = Categoria.objects.filter(
        empresa=empresa,
        activo=True,
    ).order_by("orden", "nombre")
    
    productos = Producto.objects.filter(
        empresa=empresa,
        activo=True,
        categoria__activo=True,
    ).order_by("categoria__orden", "nombre")
    
    clientes = Cliente.objects.filter(
        empresa=empresa,
        activo=True
    ).order_by("nombre")

    return render(
        request,
        "pedidos/pos.html",
        {
            "empresa": empresa,
            "categorias": categorias,
            "productos": productos,
            "clientes": clientes,
        }
    )

from django.http import JsonResponse

import json


@login_required
def crear_pedido_pos(request):

    if request.method != "POST":

        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    datos = json.loads(request.body)

    empresa = request.user.empresa_usuario.empresa
    
    if datos["cliente"]:

        cliente = Cliente.objects.get(
            id=datos["cliente"],
            empresa=empresa
        )
    
    else:
    
        cliente, creado = Cliente.objects.get_or_create(
    
            empresa=empresa,
    
            es_consumidor_final=True,
    
            defaults={
    
                "nombre": "Consumidor Final",
    
                "telefono": "",
    
                "direccion": "",
    
                "observaciones": "",
    
                "activo": True,
    
            }
    
        )
    
    pedido = Pedido.objects.create(
        empresa=empresa,
        cliente=cliente,
        estado="pendiente",
        estado_pago="pendiente",
        forma_pago="efectivo",
    )
    
    total = Decimal("0")
    
    for item in datos["productos"]:
    
        producto = Producto.objects.get(
            id=item["id"],
            empresa=empresa
        )
    
        cantidad = int(item["cantidad"])
    
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )
    
        producto.stock_reservado += cantidad
        producto.save(update_fields=["stock_reservado"])
    
        total += producto.precio * cantidad
    
    pedido.total = total
    pedido.save(update_fields=["total"])
    
    return JsonResponse({
        "ok": True,
        "pedido": pedido.numero
    })