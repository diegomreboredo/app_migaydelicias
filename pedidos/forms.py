from django import forms

from clientes.models import Cliente


class PedidoForm(forms.Form):

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.none(),
        label="Cliente"
    )

    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 3}
        )
    )

    def __init__(self, empresa, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["cliente"].queryset = (
            Cliente.objects.filter(
                empresa=empresa,
                activo=True
            )
        )