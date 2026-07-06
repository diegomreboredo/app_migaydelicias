from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import obtener_metricas



@login_required
def dashboard_reportes(request):

    empresa = request.user.empresa_usuario.empresa

    context = {
      "empresa": empresa,
      **obtener_metricas(empresa),
  }

    return render(
        request,
        "reportes/dashboard.html",
        context
    )
    
