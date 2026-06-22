from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.lista_productos,
        name="lista_productos"
    ),

    path(
        "nuevo/",
        views.nuevo_producto,
        name="nuevo_producto"
    ),
    path(
    "<int:producto_id>/editar/",
    views.editar_producto,
    name="editar_producto"
),
path(
    "<int:producto_id>/stock/",
    views.agregar_stock,
    name="agregar_stock"
),
path(
    "<int:producto_id>/movimientos/",
    views.movimientos_producto,
    name="movimientos_producto"
),
path(
    "<int:producto_id>/toggle-activo/",
    views.toggle_producto_activo,
    name="toggle_producto_activo"
),
path(
    "<int:producto_id>/ajuste/",
    views.ajuste_stock,
    name="ajuste_stock"
),

]