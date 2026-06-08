from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "empresa",
        "categoria",
        "precio",
        "stock",
        "activo",
    )

    list_filter = (
        "empresa",
        "categoria",
        "activo",
    )

    search_fields = (
        "nombre",
    )