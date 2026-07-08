from empresas.models import Empresa
from pedidos.models import Pedido

for empresa in Empresa.objects.all():

    numero = 1

    pedidos = Pedido.objects.filter(
        empresa=empresa
    ).order_by("creado")

    for pedido in pedidos:
        pedido.numero = numero
        pedido.save(update_fields=["numero"])
        numero += 1

print("Numeración corregida correctamente.")
