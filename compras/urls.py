from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.lista_compras,
        name="lista_compras"
    ),

    path(
        "nueva/",
        views.nueva_compra,
        name="nueva_compra"
    ),

    path(
        "<int:compra_id>/",
        views.detalle_compra,
        name="detalle_compra"
    ),
    path(
    "<int:compra_id>/recibir/",
    views.recibir_compra,
    name="recibir_compra",
),
path(
    "detalle/<int:detalle_id>/editar/",
    views.editar_detalle_compra,
    name="editar_detalle_compra",
),
path(
    "detalle/<int:detalle_id>/eliminar/",
    views.eliminar_detalle_compra,
    name="eliminar_detalle_compra",
),
path(
    "editar/<int:compra_id>/",
    views.editar_compra,
    name="editar_compra",
),
path(
    "cancelar/<int:compra_id>/",
    views.cancelar_compra,
    name="cancelar_compra",
),
]