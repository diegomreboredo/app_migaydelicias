from django import forms
from .models import MovimientoCaja
from .models import Caja


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
        
 


class AperturaCajaForm(forms.ModelForm):

    class Meta:
        model = Caja

        fields = [
            "saldo_inicial",
        ]

        widgets = {
            "saldo_inicial": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Ingrese el saldo inicial"
                }
            )
        }
        


class CierreCajaForm(forms.ModelForm):

    class Meta:
        model = Caja

        fields = [
            "saldo_contado",
            "observaciones_cierre",
        ]

        widgets = {
            "saldo_contado": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Ingrese el dinero contado",
                }
            ),
            "observaciones_cierre": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observaciones del cierre",
                }
            ),
        }

    def clean_saldo_contado(self):

        saldo = self.cleaned_data.get("saldo_contado")

        if saldo is None:

            raise forms.ValidationError(
                "Debe ingresar el saldo contado."
            )

        return saldo