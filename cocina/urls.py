from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.panel_cocina,
        name="panel_cocina",
    ),
]