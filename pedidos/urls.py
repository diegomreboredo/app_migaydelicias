from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.lista_pedidos,
        name="lista_pedidos"
    ),

    path(
        "nuevo/",
        views.nuevo_pedido,
        name="nuevo_pedido"
    ),
    path(
    "<int:pedido_id>/",
    views.detalle_pedido,
    name="detalle_pedido"
),
path(
    "<int:pedido_id>/estado/<str:nuevo_estado>/",
    views.cambiar_estado,
    name="cambiar_estado"
),

]