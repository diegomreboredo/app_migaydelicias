from django import forms
from .models import MovimientoCaja


class MovimientoCajaForm(forms.ModelForm):

    class Meta:
        model = MovimientoCaja
        fields = [
            "tipo",
            "concepto",
            "monto",
            "observaciones",
        ]

        widgets = {
            "tipo": forms.Select(attrs={
                "class": "form-select",
            }),
            "concepto": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "monto": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
            }),
        }