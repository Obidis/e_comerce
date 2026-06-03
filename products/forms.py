from .models import Products
from django import forms

from .models import StockMovement



class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            "product_name",
            "category",
            "supplier",
            "stock"
        ]
        widgets = {
            "category": forms.Select(choices=[
                ("Camas", "Camas"),
                ("Sillas", "Sillas"),
                ("Gruas", "Gruas"),
                ("Scooters", "Scooters"),
            ]),
            "supplier": forms.Select(choices=[
                ("Ossor", "Ossor"),
                ("Ottobock", "Ottobock"),
                ("Synthes", "Synthes"),
                ("Amoena", "Amoena"),
            ]),
        }


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'notes']

