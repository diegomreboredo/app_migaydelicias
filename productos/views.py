from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from inventario.models import MovimientoInventario
from .forms_stock import AgregarStockForm
from .forms_ajuste import AjusteStockForm

from .models import Producto
from .forms import ProductoForm


@login_required
def lista_productos(request):

    empresa = request.user.empresa_usuario.empresa

    productos = Producto.objects.filter(
        empresa=empresa
    )

    filtro = request.GET.get("filtro")

    if filtro == "activos":
        productos = productos.filter(
            activo=True
        )

    elif filtro == "inactivos":
        productos = productos.filter(
            activo=False
        )

    elif filtro == "stock_bajo":
        productos = [
            p for p in productos
            if p.stock <= p.stock_minimo
        ]

    q = request.GET.get("q")

    if q:

        if isinstance(productos, list):

            productos = [
                p for p in productos
                if q.lower() in p.nombre.lower()
            ]

        else:

            productos = productos.filter(
                nombre__icontains=q
            )

    total_productos = Producto.objects.filter(
        empresa=empresa
    ).count()

    activos_total = Producto.objects.filter(
        empresa=empresa,
        activo=True
    ).count()

    inactivos_total = Producto.objects.filter(
        empresa=empresa,
        activo=False
    ).count()

    stock_critico_total = sum(
        1
        for p in Producto.objects.filter(
            empresa=empresa
        )
        if p.stock <= p.stock_minimo
    )

    return render(
        request,
        "productos/lista.html",
        {
            "empresa": empresa,
            "productos": productos,
            "q": q,
            "total_productos": total_productos,
            "activos_total": activos_total,
            "inactivos_total": inactivos_total,
            "stock_critico_total": stock_critico_total,
        }
    )


@login_required
def nuevo_producto(request):

    empresa = request.user.empresa_usuario.empresa

    if request.method == "POST":

        form = ProductoForm(
            empresa,
            request.POST
        )

        if form.is_valid():

            producto = form.save(
                commit=False
            )

            producto.empresa = empresa

            producto.full_clean()

            producto.save()

            stock_inicial = form.cleaned_data.get(
                "stock_inicial",
                0
            )

            if stock_inicial > 0:

                MovimientoInventario.objects.create(
                    empresa=empresa,
                    producto=producto,
                    tipo="ingreso",
                    cantidad=stock_inicial,
                    motivo="Stock inicial"
                )

            return redirect(
                "lista_productos"
            )

    else:

        form = ProductoForm(
            empresa
        )

    return render(
        request,
        "productos/crear.html",
        {
            "empresa": empresa,
            "form": form,
        }
    )
    
@login_required
def editar_producto(request, producto_id):

    empresa = request.user.empresa_usuario.empresa

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        empresa=empresa
    )

    if request.method == "POST":

        form = ProductoForm(
            empresa,
            request.POST,
            request.FILES,
            instance=producto
        )

        if form.is_valid():

            producto = form.save(
                commit=False
            )

            producto.empresa = empresa

            producto.full_clean()

            producto.save()

            return redirect(
                "lista_productos"
            )

    else:

        form = ProductoForm(
            empresa,
            instance=producto
        )

    return render(
        request,
        "productos/editar.html",
        {
            "form": form,
            "producto": producto,
            "empresa": empresa,
        }
    )
    
@login_required
def agregar_stock(request, producto_id):

    empresa = request.user.empresa_usuario.empresa

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        empresa=empresa
    )

    if request.method == "POST":

        form = AgregarStockForm(
            request.POST
        )

        if form.is_valid():

            MovimientoInventario.objects.create(
                empresa=empresa,
                producto=producto,
                tipo="ingreso",
                cantidad=form.cleaned_data["cantidad"],
                motivo=form.cleaned_data["motivo"]
            )

            return redirect(
                "lista_productos"
            )

    else:

        form = AgregarStockForm()

    return render(
        request,
        "productos/agregar_stock.html",
        {
            "producto": producto,
            "form": form,
            "empresa": empresa,
        }
    )
    
@login_required
def movimientos_producto(request, producto_id):

    empresa = request.user.empresa_usuario.empresa

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        empresa=empresa
    )

    movimientos = (
        producto.movimientos_inventario.all()
    )

    return render(
        request,
        "productos/movimientos.html",
        {
            "empresa": empresa,
            "producto": producto,
            "movimientos": movimientos,
        }
    )
    
@login_required
def toggle_producto_activo(
    request,
    producto_id
):

    empresa = request.user.empresa_usuario.empresa

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        empresa=empresa
    )

    producto.activo = not producto.activo

    producto.save(
        update_fields=["activo"]
    )

    return redirect(
        "lista_productos"
    )
    
@login_required
def ajuste_stock(request, producto_id):

    empresa = request.user.empresa_usuario.empresa

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        empresa=empresa
    )

    if request.method == "POST":

        form = AjusteStockForm(
            request.POST
        )

        if form.is_valid():

            MovimientoInventario.objects.create(
                empresa=empresa,
                producto=producto,
                tipo="merma",
                cantidad=form.cleaned_data["cantidad"],
                motivo=form.cleaned_data["motivo"]
            )

            return redirect(
                "lista_productos"
            )

    else:

        form = AjusteStockForm()

    return render(
        request,
        "productos/ajuste_stock.html",
        {
            "empresa": empresa,
            "producto": producto,
            "form": form,
        }
    )