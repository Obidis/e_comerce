from django.db import models, transaction
from django.contrib.auth.models import User

from django.conf import settings
from django.core.validators import MinValueValidator



class Products(models.Model):
    product = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="products", verbose_name=("Producto"))
    product_name = models.CharField(max_length=50, blank=True, verbose_name=("Nombre"))
    category = models.CharField(max_length=100, blank=True, verbose_name=("Categoria"))
    supplier = models.CharField(max_length=50, blank=True, verbose_name=("Proveedor"))
    timestamp  = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=("Fecha"))
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name=("Stock/Cantidad"))
   
    
    
    class Meta:
               
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


    def __str__(self):
        return self.product_name
    








class StockMovement(models.Model):
    MOVEMENT_TYPES = (('IN', 'Entrada'), ('OUT', 'Salida'),)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='movements', verbose_name="Producto")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movements', null=True, blank=True, verbose_name="Usuario")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad")
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES, verbose_name="Tipo de movimiento")
    notes = models.CharField(max_length=100, blank=True, help_text="Razón del movimiento (ej. Factura #123, Inventario físico)")
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Fecha")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.movement_type} - {self.product.product_name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # Lógica para actualizar el stock del producto automáticamente
        is_new = self.pk is None

        with transaction.atomic():
            if is_new:
                if self.product.stock is None:
                    self.product.stock = 0
                if self.movement_type == 'IN':
                    self.product.stock += self.quantity
                elif self.movement_type == 'OUT':
                    if self.product.stock < self.quantity:
                        from django.core.exceptions import ValidationError
                        raise ValidationError(
                            f"Stock insuficiente. Disponible: {self.product.stock}, solicitado: {self.quantity}"
                        )
                    self.product.stock -= self.quantity
                self.product.save(update_fields=['stock'])

            super().save(*args, **kwargs)

   