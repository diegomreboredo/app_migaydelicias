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
]