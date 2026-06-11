from django.contrib import admin

from .models import Compra, DetalleCompra


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "empresa",
        "proveedor",
        "estado",
        "total",
        "creado",
    )

    list_filter = (
        "empresa",
        "estado",
    )

    search_fields = (
        "id",
        "proveedor__nombre",
    )

    inlines = [
        DetalleCompraInline
    ]


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):

    list_display = (
        "compra",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal",
    )