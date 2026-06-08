from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "empresa",
        "telefono",
        "activo"
    )

    list_filter = (
        "empresa",
        "activo"
    )

    search_fields = (
        "nombre",
        "telefono"
    )