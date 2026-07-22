from django.urls import path
from . import views

urlpatterns = [
    path(
        "movimientos/",
        views.lista_caja,
        name="lista_caja",
    ),
    path(
    "nuevo/",
    views.nuevo_movimiento,
    name="nuevo_movimiento",
),
path(
    "",
    views.inicio_caja,
    name="inicio_caja",
),
path(
    "abrir/",
    views.abrir_caja,
    name="abrir_caja",
),
path(
    "cerrar/",
    views.cerrar_caja,
    name="cerrar_caja",
),
path(
    "historial/",
    views.historial_cajas,
    name="historial_cajas",
),
path(
    "historial/<int:pk>/",
    views.detalle_caja,
    name="detalle_caja",
),
]