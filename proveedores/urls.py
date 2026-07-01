from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.lista_proveedores,
        name="lista_proveedores"
    ),

    path(
        "nuevo/",
        views.nuevo_proveedor,
        name="nuevo_proveedor"
    ),

    path(
        "<int:proveedor_id>/editar/",
        views.editar_proveedor,
        name="editar_proveedor"
    ),
    path(
    "<int:proveedor_id>/toggle/",
    views.toggle_proveedor,
    name="toggle_proveedor"
),

]