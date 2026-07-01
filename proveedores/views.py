from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Proveedor
from .forms import ProveedorForm


@login_required
def lista_proveedores(request):

    empresa = request.user.empresa_usuario.empresa

    proveedores = Proveedor.objects.filter(
        empresa=empresa
    )

    q = request.GET.get("q")

    if q:
        proveedores = proveedores.filter(
            nombre__icontains=q
        )

    total = proveedores.count()

    activos = proveedores.filter(
        activo=True
    ).count()

    inactivos = total - activos
    
    q = request.GET.get("q")

    if q:
        proveedores = proveedores.filter(
            nombre__icontains=q
        )
    
    filtro = request.GET.get("filtro")
    
    if filtro == "activos":
    
        proveedores = proveedores.filter(
            activo=True
        )
    
    elif filtro == "inactivos":
    
        proveedores = proveedores.filter(
            activo=False
        )

    return render(
        request,
        "proveedores/lista.html",
        {
            "empresa": empresa,
            "proveedores": proveedores,
            "q": q,
            "total": total,
            "activos": activos,
            "inactivos": inactivos,
            "filtro": filtro,
        }
    )


@login_required
def nuevo_proveedor(request):

    empresa = request.user.empresa_usuario.empresa

    if request.method == "POST":

        form = ProveedorForm(request.POST)

        if form.is_valid():

            proveedor = form.save(commit=False)

            proveedor.empresa = empresa

            proveedor.save()

            return redirect("lista_proveedores")

    else:

        form = ProveedorForm()

    return render(
        request,
        "proveedores/crear.html",
        {
            "empresa": empresa,
            "form": form,
        }
    )


@login_required
def editar_proveedor(request, proveedor_id):

    empresa = request.user.empresa_usuario.empresa

    proveedor = get_object_or_404(
        Proveedor,
        id=proveedor_id,
        empresa=empresa
    )

    if request.method == "POST":

        form = ProveedorForm(
            request.POST,
            instance=proveedor
        )

        if form.is_valid():

            proveedor = form.save(commit=False)

            proveedor.empresa = empresa

            proveedor.save()

            return redirect("lista_proveedores")

    else:

        form = ProveedorForm(
            instance=proveedor
        )

    return render(
        request,
        "proveedores/editar.html",
        {
            "empresa": empresa,
            "form": form,
            "proveedor": proveedor,
        }
    )
    
from django.http import JsonResponse


@login_required
def toggle_proveedor(request, proveedor_id):

    empresa = request.user.empresa_usuario.empresa

    proveedor = get_object_or_404(
        Proveedor,
        id=proveedor_id,
        empresa=empresa
    )

    proveedor.activo = not proveedor.activo

    proveedor.save()

    return JsonResponse({
        "activo": proveedor.activo
    })