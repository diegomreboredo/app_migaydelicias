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
    
    def get_readonly_fields(self, request, obj=None):

      if obj:
          return (
              "empresa",
              "producto",
              "tipo",
              "cantidad",
              "motivo",
              "referencia",
              "creado",
          )
  
      return ()
    
    def has_delete_permission(self, request, obj=None):
      return False