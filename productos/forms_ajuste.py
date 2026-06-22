from django import forms

class AjusteStockForm(forms.Form):

    cantidad = forms.IntegerField(
        min_value=1,
        label="Cantidad"
    )

    motivo = forms.CharField(
        label="Motivo"
    )