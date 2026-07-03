from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CompraForm, DetalleCompraForm
from .models import Compra, DetalleCompra


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

    proveedor_id = request.GET.get("proveedor")
    

    form = CompraForm(request.POST or None)

    queryset = empresa.proveedores.filter(activo=True)

    form.fields["proveedor"].queryset = queryset

    # 🔥 ESTE ES EL FIX REAL
    if proveedor_id:
        form.fields["proveedor"].initial = proveedor_id

    if request.method == "POST":

        if form.is_valid():

            compra = form.save(commit=False)
            compra.empresa = empresa
            compra.full_clean()
            compra.save()

            return redirect("detalle_compra", compra.id)

    return render(request, "compras/crear.html", {
        "form": form
    })
    
@login_required
def editar_compra(request, compra_id):

    empresa = request.user.empresa_usuario.empresa

    compra = get_object_or_404(
        Compra,
        pk=compra_id,
        empresa=empresa,
    )

    # No permitir editar compras ya recibidas
    if compra.estado == "recibida":
        return redirect(
            "detalle_compra",
            compra_id=compra.id
        )

    if request.method == "POST":

        form = CompraForm(
            request.POST,
            instance=compra
        )

        form.fields["proveedor"].queryset = (
            empresa.proveedores.filter(activo=True)
        )

        if form.is_valid():

            form.save()

            return redirect(
                "detalle_compra",
                compra_id=compra.id
            )

    else:

        form = CompraForm(instance=compra)

        form.fields["proveedor"].queryset = (
            empresa.proveedores.filter(activo=True)
        )

    return render(
        request,
        "compras/editar.html",
        {
            "form": form,
            "compra": compra,
        },
    )
    
@login_required
def cancelar_compra(request, compra_id):

    compra = get_object_or_404(
        Compra,
        pk=compra_id
    )

    if compra.estado != "pendiente":
        return redirect("detalle_compra", compra.id)

    if request.method == "POST":

        compra.estado = "cancelada"
        compra.save()

        return redirect("lista_compras")

    return render(
        request,
        "compras/cancelar.html",
        {
            "compra": compra
        }
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
    
@login_required
def editar_detalle_compra(request, detalle_id):

    detalle = get_object_or_404(
        DetalleCompra,
        pk=detalle_id
    )
    
    if detalle.compra.estado == "recibida":
          return redirect(
              "detalle_compra",
              compra_id=detalle.compra.id
          )

    if request.method == "POST":

        form = DetalleCompraForm(
            request.POST,
            instance=detalle
        )

        form.fields["producto"].queryset = (
            detalle.compra.empresa.productos.filter(
                activo=True
            )
        )

        if form.is_valid():

            form.save()

            return redirect(
                "detalle_compra",
                compra_id=detalle.compra.id
            )

    else:

        form = DetalleCompraForm(
            instance=detalle
        )

        form.fields["producto"].queryset = (
            detalle.compra.empresa.productos.filter(
                activo=True
            )
        )

    return render(
        request,
        "compras/editar_detalle.html",
        {
            "form": form,
            "detalle": detalle,
        }
    )

@login_required
def eliminar_detalle_compra(request, detalle_id):

    detalle = get_object_or_404(
        DetalleCompra,
        pk=detalle_id
    )

    if detalle.compra.estado == "recibida":
        return redirect(
            "detalle_compra",
            compra_id=detalle.compra.id
        )

    compra_id = detalle.compra.id

    detalle.delete()

    return redirect(
        "detalle_compra",
        compra_id=compra_id
    )