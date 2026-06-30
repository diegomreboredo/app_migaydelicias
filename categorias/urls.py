from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.lista_categorias,
        name="lista_categorias"
    ),

    path(
        "nuevo/",
        views.nueva_categoria,
        name="nueva_categoria"
    ),

    path(
        "<int:categoria_id>/editar/",
        views.editar_categoria,
        name="editar_categoria"
    ),

    path(
        "<int:categoria_id>/toggle-activo/",
        views.toggle_categoria,
        name="toggle_categoria"
    ),

]