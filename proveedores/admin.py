from django.contrib import admin

from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "empresa",
        "telefono",
        "email",
        "activo",
    )

    list_filter = (
        "empresa",
        "activo",
    )

    search_fields = (
        "nombre",
        "razon_social",
        "cuit",
        "telefono",
        "email",
    )

    ordering = (
        "nombre",
    )