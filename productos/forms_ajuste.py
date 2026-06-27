from django import forms


class AjusteStockForm(forms.Form):

    MOTIVOS = [
        ("vencido", "🟠 Producto vencido"),
        ("rotura", "🔴 Rotura"),
        ("merma", "📦 Merma"),
        ("donacion", "🎁 Donación"),
        ("ajuste", "⚙ Ajuste de inventario"),
        ("otro", "✏ Otro"),
    ]

    cantidad = forms.IntegerField(
        min_value=1,
        label="Cantidad"
    )

    motivo = forms.ChoiceField(
        choices=MOTIVOS,
        label="Motivo"
    )

    observacion = forms.CharField(
        required=False,
        label="Observación"
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["cantidad"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Ingrese la cantidad"
        })

        self.fields["motivo"].widget.attrs.update({
            "class": "form-select",
            "id": "id_motivo"
        })

        self.fields["observacion"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Solo si selecciona 'Otro'",
            "id": "id_observacion"
        })