from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render

from productos.models import Producto


@login_required
def lista_inventario(request):

    empresa = request.user.empresa_usuario.empresa

    productos = Producto.objects.filter(
        empresa=empresa
    ).select_related("categoria")

    q = request.GET.get("q")

    if q:
        productos = productos.filter(
            nombre__icontains=q
        )

    filtro = request.GET.get("filtro")

    if filtro == "sin_stock":

        productos = productos.filter(
            stock=0
        )

    elif filtro == "stock_critico":

        productos = productos.filter(
            stock__gt=0,
            stock__lte=models.F("stock_minimo")
        )

    elif filtro == "stock_normal":

        productos = productos.filter(
            stock__gt=models.F("stock_minimo")
        )

    total_productos = Producto.objects.filter(
        empresa=empresa
    ).count()

    sin_stock = Producto.objects.filter(
        empresa=empresa,
        stock=0
    ).count()

    stock_critico = Producto.objects.filter(
        empresa=empresa,
        stock__gt=0,
        stock__lte=models.F("stock_minimo")
    ).count()

    stock_normal = (
        total_productos
        - sin_stock
        - stock_critico
    )

    return render(
        request,
        "inventario/lista.html",
        {
            "empresa": empresa,
            "productos": productos,
            "total_productos": total_productos,
            "sin_stock": sin_stock,
            "stock_critico": stock_critico,
            "stock_normal": stock_normal,
            "filtro": filtro,
            "q": q,
        }
    )