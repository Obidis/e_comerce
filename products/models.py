from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.core.validators import MinValueValidator



class Products(models.Model):
    product = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="products", verbose_name=("Producto"))
    product_name = models.CharField(max_length=50, blank=True, verbose_name=("Nombre"))
    category = models.CharField(max_length=100, blank=True, verbose_name=("Categoria"))
    supplier = models.CharField(max_length=50, blank=True, verbose_name=("Proveedor"))
    timestamp  = models.DateTimeField(auto_now_add=True,  blank=True, verbose_name=("Fecha"))
    stock = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=("Stock/Cantidad"))
   
    
    
    class Meta:
               
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


    def __str__(self):
        return self.product_name
    



from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator



class StockMovement(Products, models.Model):
    MOVEMENT_TYPES = (('IN', 'Entrada'), ('OUT', 'Salida'),)
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    notes = models.TextField(blank=True, help_text="Razón del movimiento (ej. Factura #123, Inventario físico)")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.movement_type} - {self.product_name} ({self.stock})"

    def save(self, *args, **kwargs):
        # Lógica para actualizar el stock del producto automáticamente
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            if self.movement_type == 'IN':
                self.stock += self.stock
            elif self.movement_type == 'OUT':
                self.stock -= self.stock
            self.product.save()

   