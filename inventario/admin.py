from django.contrib import admin

from .models import MovimientoInventario


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "empresa",
        "producto",
        "tipo",
        "cantidad",
        "referencia",
        "creado",
    )

    list_filter = (
        "empresa",
        "tipo",
    )

    search_fields = (
        "producto__nombre",
        "motivo",
        "referencia"
    )

    ordering = (
        "-creado",
    )