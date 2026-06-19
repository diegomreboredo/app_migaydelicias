from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import ClienteForm

from .models import Cliente

from django.shortcuts import get_object_or_404


@login_required
def editar_cliente(request, pk):

    empresa = request.user.empresa_usuario.empresa

    cliente = get_object_or_404(
        Cliente,
        pk=pk,
        empresa=empresa
    )

    if request.method == "POST":

        form = ClienteForm(
            request.POST,
            instance=cliente
        )

        if form.is_valid():

            form.save()

            return redirect(
                "lista_clientes"
            )

    else:

        form = ClienteForm(
            instance=cliente
        )

    return render(
        request,
        "clientes/editar.html",
        {
            "form": form,
            "cliente": cliente
        }
    )


@login_required
def lista_clientes(request):

    empresa = request.user.empresa_usuario.empresa

    clientes = Cliente.objects.filter(
        empresa=empresa,
        activo=True
    )

    context = {
        "empresa": empresa,
        "clientes": clientes,
    }

    return render(
        request,
        "clientes/lista.html",
        context
    )
    
    
@login_required
def crear_cliente(request):

    empresa = request.user.empresa_usuario.empresa

    if request.method == "POST":

        form = ClienteForm(request.POST)

        if form.is_valid():

            cliente = form.save(commit=False)

            cliente.empresa = empresa

            cliente.save()

        return redirect("lista_clientes")

    else:

        form = ClienteForm()

    return render(
        request,
        "clientes/crear.html",
        {
            "form": form
        }
    )
    
@login_required
def eliminar_cliente(request, pk):

    empresa = request.user.empresa_usuario.empresa

    cliente = get_object_or_404(
        Cliente,
        pk=pk,
        empresa=empresa
    )

    cliente.activo = False

    cliente.save()

    return redirect(
        "lista_clientes"
    )