from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CompraForm, DetalleCompraForm
from .models import Compra


@login_required
def lista_compras(request):

    empresa = request.user.empresa_usuario.empresa

    compras = Compra.objects.filter(
        empresa=empresa
    ).select_related("proveedor")

    q = request.GET.get("q")

    if q:

        compras = compras.filter(
            proveedor__nombre__icontains=q
        )

    filtro = request.GET.get("filtro")

    if filtro == "pendientes":

        compras = compras.filter(
            estado="pendiente"
        )

    elif filtro == "recibidas":

        compras = compras.filter(
            estado="recibida"
        )

    elif filtro == "canceladas":

        compras = compras.filter(
            estado="cancelada"
        )

    total = Compra.objects.filter(
        empresa=empresa
    ).count()

    pendientes = Compra.objects.filter(
        empresa=empresa,
        estado="pendiente"
    ).count()

    recibidas = Compra.objects.filter(
        empresa=empresa,
        estado="recibida"
    ).count()

    canceladas = Compra.objects.filter(
        empresa=empresa,
        estado="cancelada"
    ).count()

    return render(
        request,
        "compras/lista.html",
        {
            "empresa": empresa,
            "compras": compras,
            "total": total,
            "pendientes": pendientes,
            "recibidas": recibidas,
            "canceladas": canceladas,
            "filtro": filtro,
        },
    )


@login_required
def nueva_compra(request):

    empresa = request.user.empresa_usuario.empresa

    if request.method == "POST":

        form = CompraForm(request.POST)

        if form.is_valid():
        
            compra = form.save(commit=False)
        
            compra.empresa = empresa
        
            compra.full_clean()
        
            compra.save()

            return redirect(
                "detalle_compra",
                compra.id
            )

    else:

        form = CompraForm()

        form.fields["proveedor"].queryset = (
            empresa.proveedores.filter(
                activo=True
            )
        )

    return render(
        request,
        "compras/crear.html",
        {
            "form": form
        },
    )
    
@login_required
def detalle_compra(request, compra_id):

    compra = get_object_or_404(
        Compra,
        pk=compra_id
    )

    if request.method == "POST":

        form = DetalleCompraForm(request.POST)

        form.fields["producto"].queryset = (
            compra.empresa.productos.filter(
                activo=True
            )
        )

        if form.is_valid():

            detalle = form.save(commit=False)

            detalle.compra = compra

            detalle.save()

            return redirect(
                "detalle_compra",
                compra.id
            )

    else:

        form = DetalleCompraForm()

        form.fields["producto"].queryset = (
            compra.empresa.productos.filter(
                activo=True
            )
        )

    return render(
        request,
        "compras/detalle.html",
        {
            "compra": compra,
            "form": form,
        }
    )
    
@login_required
def recibir_compra(request, compra_id):

    compra = get_object_or_404(
        Compra,
        pk=compra_id
    )

    if request.method == "POST":

        compra.estado = "recibida"

        compra.save()

    return redirect(
        "detalle_compra",
        compra.id
    )