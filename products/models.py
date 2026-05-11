from django.db import models
from django.contrib.auth.models import User


class Products(models.Model):
    product = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="products", verbose_name=("Producto"))
    product_name = models.CharField(max_length=50, blank=True, verbose_name=("Nombre"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=("Precio"))
    image = models.ImageField(upload_to="product_images/", verbose_name=("Imagen"))
    description = models.TextField(max_length=3000, blank=True, verbose_name=("Descripcion"))
    supplier = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="products_supplied", verbose_name=("Proveedor"))
    add_at = models.DateTimeField(auto_now_add=True, verbose_name=("Fecha de entrada"))
    stock = models.PositiveIntegerField(default=0, verbose_name=("Stock/Cantidad"))
    cart = models.ManyToManyField(User, related_name='favourite', verbose_name=("Cesta"), blank=True)


    class Meta:
               
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


    def __str__(self):
        return self.product_name