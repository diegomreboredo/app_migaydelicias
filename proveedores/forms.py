from django import forms
from .models import Proveedor


class ProveedorForm(forms.ModelForm):

    class Meta:

        model = Proveedor

        fields = [
            "nombre",
            "razon_social",
            "cuit",
            "contacto",
            "telefono",
            "email",
            "direccion",
            "ciudad",
            "provincia",
            "observaciones",
            "activo",
        ]

        widgets = {

            "nombre": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "razon_social": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "cuit": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "contacto": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "telefono": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "direccion": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "ciudad": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "provincia": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "activo": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }