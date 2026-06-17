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
  
  context = {
  
      "empresa": empresa,
  
      "pendientes": pendientes,
  
      "preparacion": preparacion,
  
      "listos": listos,
  
      "entregados": entregados,
  }
  
  return render(
      request,
      "pedidos/lista.html",
      context
  )