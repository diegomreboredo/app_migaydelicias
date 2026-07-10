from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm
from .models import Categoria
from .emojis import EMOJIS_GASTRONOMIA


@login_required
def lista_categorias(request):

    empresa = request.user.empresa_usuario.empresa

    categorias = Categoria.objects.filter(
        empresa=empresa
    ).annotate(
        total_productos=Count("productos")
    )

    q = request.GET.get("q")

    if q:
        categorias = categorias.filter(
            nombre__icontains=q
        )

    total = Categoria.objects.filter(
        empresa=empresa
    ).count()

    activas = Categoria.objects.filter(
        empresa=empresa,
        activo=True
    ).count()

    inactivas = total - activas

    return render(
        request,
        "categorias/lista.html",
        {
            "empresa": empresa,
            "categorias": categorias,
            "total": total,
            "activas": activas,
            "inactivas": inactivas,
            "q": q,
        }
    )


@login_required
def crear_categoria(request):

    empresa = request.user.empresa_usuario.empresa
    
    print("=== CREAR CATEGORIA ===")
    print("METHOD:", request.method)
    print("GET next:", request.GET.get("next"))
    print("GET select:", request.GET.get("select"))

    if request.method == "POST":

        form = CategoriaForm(request.POST)

        if form.is_valid():

            categoria = form.save(commit=False)
            categoria.empresa = empresa
            categoria.icono = request.POST.get("icono", "🍽️")
            categoria.save()
            
            next_url = request.GET.get("next")
            select = request.GET.get("select")
            
            if next_url:
                if select:
                    sep = "&" if "?" in next_url else "?"
                    return redirect(f"{next_url}{sep}categoria={categoria.id}")
            
                return redirect(next_url)
            
            return redirect("lista_categorias")

            messages.success(
                request,
                "Categoría creada correctamente."
            )

            return redirect("lista_categorias")

    else:

        form = CategoriaForm()

    return render(
        request,
        "categorias/crear.html",
        {
            "empresa": empresa,
            "form": form,
            "emojis": EMOJIS_GASTRONOMIA,
        }
    )


@login_required
def editar_categoria(request, categoria_id):

    empresa = request.user.empresa_usuario.empresa

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id,
        empresa=empresa
    )

    if request.method == "POST":

        form = CategoriaForm(
            request.POST,
            instance=categoria
        )

        if form.is_valid():

            categoria.icono = request.POST.get("icono", categoria.icono)
            form.save()

            messages.success(
                request,
                "Categoría actualizada."
            )

            return redirect("lista_categorias")

    else:

        form = CategoriaForm(instance=categoria)

    return render(
        request,
        "categorias/editar.html",
        {
            "empresa": empresa,
            "form": form,
            "categoria": categoria,
            "emojis": EMOJIS_GASTRONOMIA,
        }
    )


@login_required
def toggle_categoria(request, categoria_id):

    empresa = request.user.empresa_usuario.empresa

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id,
        empresa=empresa
    )

    categoria.activo = not categoria.activo
    categoria.save(update_fields=["activo"])

    return redirect("lista_categorias")