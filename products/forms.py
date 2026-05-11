from .models import Products
from django import forms



class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            "image",
            "product_name",
            "description",
            "supplier",
            "price",
            "stock"
        ]
