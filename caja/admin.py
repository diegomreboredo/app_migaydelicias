from django.contrib import admin

from .models import MovimientoCaja


@admin.register(MovimientoCaja)
class MovimientoCajaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "empresa",
        "tipo",
        "concepto",
        "referencia",
        "monto",
        "creado",
    )

    list_filter = (
        "empresa",
        "tipo",
    )

    search_fields = (
        "concepto",
    )

    ordering = (
        "-creado",
    )