from django.contrib import admin
from products.models import Products


# Register your models here.

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["product_name", "stock"]
    list_filter = ["product_name", "stock"]
    search_fields = ["product_name"]
    ordering = ["product_name"]

class StockMovementAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "movement_type", "timestamp", "user", "notes"]
    list_filter = ["movement_type", "timestamp"]
    search_fields = ["product__product_name", "notes"]
    ordering = ["-timestamp"]

    