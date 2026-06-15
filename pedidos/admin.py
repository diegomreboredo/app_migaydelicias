from django.contrib import admin
from .models import Pedido, DetallePedido

from django import forms
from productos.models import Producto


class DetallePedidoForm(forms.ModelForm):

    class Meta:
        model = DetallePedido
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["producto"].queryset = (
            Producto.objects.all().order_by(
                "empresa__nombre",
                "nombre"
            )
        )

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    form = DetallePedidoForm
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "empresa",
        "cliente",
        "estado",
        "total",
        "creado"
    )

    list_filter = (
        "empresa",
        "estado"
    )

    search_fields = (
        "id",
        "cliente__nombre"
    )

    def get_form(self, request, obj=None, **kwargs):
      request._pedido_obj = obj
      return super().get_form(request, obj, **kwargs)
      
    def has_delete_permission(self, request, obj=None):

        if obj and obj.estado == "entregado":
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
  
      if obj and obj.estado == "entregado":
  
          return (
              "empresa",
              "cliente",
              "estado",
              "observaciones",
              "total",
          )
  
      return ()

    inlines = [
        DetallePedidoInline
    ]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = (
        "pedido",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal"
    )