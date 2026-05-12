from .models import Products
from django import forms



class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            "product_name",
            "category",
            "supplier",
            "stock"
        ]
