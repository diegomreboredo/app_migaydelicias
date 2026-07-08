from compras.models import Compra
from empresas.models import Empresa

for empresa in Empresa.objects.all():

    numero = 1

    compras = Compra.objects.filter(
        empresa=empresa
    ).order_by("creado")

    for compra in compras:

        compra.numero = numero
        compra.save(update_fields=["numero"])

        numero += 1

print("Numeración de compras corregida correctamente.")
