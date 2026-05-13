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
        fields = ['product_name', 'movement_type', 'stock', 'id', 'notes']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        movement_type = cleaned_data.get('movement_type')
        quantity = cleaned_data.get('quantity')
        stock = cleaned_data.get('stock')
        
        if product and movement_type == StockMovement.MovementType.OUT and quantity:
            if stock < quantity:
                raise forms.ValidationError(
                    f"No hay suficiente stock. Disponible actualmente: {stock}"
                )
        return cleaned_data
