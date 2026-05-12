from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Products(models.Model):
    product = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="products", verbose_name=("Producto"))
    product_name = models.CharField(max_length=50, blank=True, verbose_name=("Nombre"))
    category = models.CharField(max_length=100, blank=True, verbose_name=("Categoria"))
    supplier = models.CharField(max_length=50, blank=True, verbose_name=("Proveedor"))
    add_at = models.DateTimeField(auto_now_add=True,  blank=True, verbose_name=("Fecha de entrada"))
    exit_at = models.DateTimeField(auto_now_add=True,  blank=True, null=True, verbose_name=("Fecha de salida"))
    stock = models.PositiveIntegerField(default=0, verbose_name=("Stock/Cantidad"))
    
    


    class Meta:
               
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


    def __str__(self):
        return self.product_name