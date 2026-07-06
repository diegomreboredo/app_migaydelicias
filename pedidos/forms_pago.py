from django import forms

from .models import Pedido


class FormaPagoForm(forms.Form):

    forma_pago = forms.ChoiceField(
        choices=Pedido.FORMAS_PAGO,
        label="Forma de pago",
        widget=forms.RadioSelect
    )