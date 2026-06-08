from django.contrib import admin
from .models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "empresa",
        "activo",
    )

    list_filter = (
        "empresa",
        "activo",
    )

    search_fields = (
        "nombre",
    )