from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.lista_caja,
        name="lista_caja",
    ),
    path(
    "nuevo/",
    views.nuevo_movimiento,
    name="nuevo_movimiento",
),
]