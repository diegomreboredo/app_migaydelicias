from django import forms

from productos.models import Producto


class DetallePedidoForm(forms.Form):

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(),
        label="Producto"
    )

    cantidad = forms.IntegerField(
        min_value=1,
        initial=1
    )

    def __init__(self, empresa, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["producto"].queryset = (
            Producto.objects.filter(
                empresa=empresa,
                activo=True
            ).order_by("nombre")
        )

        self.fields["producto"].widget.attrs.update({
            "class": "form-select",
            "id": "producto-select"
        })

        self.fields["cantidad"].widget.attrs.update({
            "class": "form-control"
        })

    def clean(self):

        cleaned_data = super().clean()

        producto = cleaned_data.get("producto")
        cantidad = cleaned_data.get("cantidad")

        if producto and cantidad:

            if cantidad > producto.stock_disponible:

                raise forms.ValidationError(
                    f"Stock insuficiente. Disponible: {producto.stock_disponible}"
                )

        return cleaned_data