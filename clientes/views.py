from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import ClienteForm
from .models import Cliente
from django.shortcuts import get_object_or_404
from pedidos.models import Pedido

@login_required
def detalle_cliente(request, pk):

    empresa = request.user.empresa_usuario.empresa

    cliente = get_object_or_404(
        Cliente,
        pk=pk,
        empresa=empresa
    )

    pedidos = (
        Pedido.objects.filter(
            empresa=empresa,
            cliente=cliente
        )
        .order_by("-creado")
    )

    total_comprado = sum(
        pedido.total for pedido in pedidos
    )

    cantidad_pedidos = pedidos.count()

    ultimo_pedido = pedidos.first()

    context = {
        "cliente": cliente,
        "pedidos": pedidos,
        "total_comprado": total_comprado,
        "cantidad_pedidos": cantidad_pedidos,
        "ultimo_pedido": ultimo_pedido,
    }

    return render(
        request,
        "clientes/detalle.html",
        context
    )


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
            
            next_url = request.GET.get("next")
            select = request.GET.get("select")
            
            if next_url:
              print("NEXT:", next_url)
              print("CLIENTE:", cliente.id)
              print("SELECT:", select)

              if select:
          
                  separador = "&" if "?" in next_url else "?"
          
                  return redirect(
                      f"{next_url}{separador}cliente={cliente.id}"
                  )
          
              return redirect(next_url)
            
            return redirect("lista_clientes")

        return redirect("lista_clientes")

    else:

        form = ClienteForm()

    return render(
    request,
    "clientes/crear.html",
    {
        "form": form,
        "empresa": empresa,
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