from django import forms

from .models import Producto
from categorias.models import Categoria


class ProductoForm(forms.ModelForm):
  
    stock_inicial = forms.IntegerField(
      required=False,
      min_value=0,
      initial=0,
      label="Stock inicial"
  )

    class Meta:

        model = Producto

        fields = [
            "categoria",
            "nombre",
            "descripcion",
            "precio",
            "stock_minimo",
            "activo",
        ]

    def __init__(self, empresa, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["categoria"].queryset = (
            Categoria.objects.filter(
                empresa=empresa,
                activo=True
            )
        )