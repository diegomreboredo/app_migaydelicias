from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import obtener_metricas
import json
from django.core.serializers.json import DjangoJSONEncoder



@login_required
def dashboard_reportes(request):

    empresa = request.user.empresa_usuario.empresa

    context = {
      "empresa": empresa,
      **obtener_metricas(empresa),
  }
  
    context["ventas_30_dias_json"] = json.dumps(
      context["ventas_30_dias"],
      cls=DjangoJSONEncoder
  )
    
    context["formas_pago_json"] = json.dumps(
        context["formas_pago"]
    )
    
    context["top_productos_json"] = json.dumps(
        context["top_productos"]
    )
    
    clientes = context["top_clientes"]

    for cliente in clientes:
        cliente["total"] = float(cliente["total"])
    
    context["top_clientes_json"] = json.dumps(clientes)
    return render(
        request,
        "reportes/dashboard.html",
        context
    )
    
