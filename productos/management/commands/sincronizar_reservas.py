from django.core.management.base import BaseCommand

from productos.models import Producto
from pedidos.models import Pedido


class Command(BaseCommand):

    help = "Reconstruye el stock reservado de todos los productos"

    def handle(self, *args, **kwargs):

        Producto.objects.update(stock_reservado=0)

        pedidos = Pedido.objects.filter(
            estado__in=[
                "pendiente",
                "preparacion",
                "listo",
            ]
        )

        for pedido in pedidos:

            for detalle in pedido.detalles.all():

                producto = detalle.producto

                producto.stock_reservado += detalle.cantidad

                producto.save(
                    update_fields=["stock_reservado"]
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Reservas sincronizadas correctamente."
            )
        )