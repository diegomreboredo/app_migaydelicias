from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Pedido

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