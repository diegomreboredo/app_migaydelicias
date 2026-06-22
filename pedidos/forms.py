from django import forms

from clientes.models import Cliente
from productos.models import Producto


class PedidoForm(forms.Form):

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.none(),
        label="Cliente"
    )

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(),
        label="Producto"
    )

    cantidad = forms.IntegerField(
        min_value=1,
        initial=1
    )

    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3
            }
        )
    )
    
    def clean(self):

        cleaned_data = super().clean()
    
        producto = cleaned_data.get("producto")
        cantidad = cleaned_data.get("cantidad")
    
        if producto and cantidad:
    
            if cantidad > producto.stock:
    
                raise forms.ValidationError(
    f"No hay stock suficiente para realizar este pedido. Disponible: {producto.stock} unidades."
)
    
        return cleaned_data

    def __init__(self, empresa, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["cliente"].queryset = (
            Cliente.objects.filter(
                empresa=empresa,
                activo=True
            )
        )

        self.fields["producto"].queryset = (
            Producto.objects.filter(
                empresa=empresa,
                activo=True
            )
        )