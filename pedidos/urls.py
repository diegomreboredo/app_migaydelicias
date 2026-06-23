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
path(
    "<int:pedido_id>/agregar-producto/",
    views.agregar_producto_pedido,
    name="agregar_producto_pedido"
),
path(
    "detalle/<int:detalle_id>/eliminar/",
    views.eliminar_detalle_pedido,
    name="eliminar_detalle_pedido"
),
path(
    "detalle/<int:detalle_id>/sumar/",
    views.sumar_cantidad_detalle,
    name="sumar_cantidad_detalle"
),

path(
    "detalle/<int:detalle_id>/restar/",
    views.restar_cantidad_detalle,
    name="restar_cantidad_detalle"
),

]