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

    def has_delete_permission(
        self,
        request,
        obj=None
    ):

        if obj and obj.referencia:
            return False

        return super().has_delete_permission(
            request,
            obj
        )

    def get_readonly_fields(
        self,
        request,
        obj=None
    ):

        if obj and obj.referencia:

            return (
                "empresa",
                "tipo",
                "concepto",
                "referencia",
                "monto",
                "observaciones",
            )

        return ()