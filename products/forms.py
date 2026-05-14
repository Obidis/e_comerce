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


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'notes']

