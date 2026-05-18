from django.db.models import Q
from django.views.generic import ListView
from products.models import Products, StockMovement
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from products.forms import ProductCreateForm, StockMovementForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
import csv
from django.http import HttpResponse
from django.shortcuts import render





#Agregar productos
@method_decorator(login_required, name="dispatch")
class ProductCreateView(CreateView):
    template_name = "products/products_add.html"
    model = Products
    form_class = ProductCreateForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.product = self.request.user

        messages.add_message(self.request, messages.SUCCESS, ('Producto creado correctamente.'))
        return super(ProductCreateView, self).form_valid(form)


#Eliminar productos
@method_decorator(login_required, name="dispatch")    
class ProductDeleteView(DeleteView):
    model = Products
    template_name ="products/products_delete.html"
    success_url = reverse_lazy('products_list')

    def get_queryset(self):
        return self.model.objects.filter(product=self.request.user)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Producto eliminado correctamente.')
        return super(ProductDeleteView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('products_list')
    
#Actualizacion de productos
@method_decorator(login_required, name="dispatch")
class ProductUpdateView(UpdateView):
    model = Products
    template_name = "products/products_update.html"
    fields = "product_name", "category", "supplier", "stock"
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(product=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, ('Producto editado correctamente.'))
        return super(ProductUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('home')

# Listado de producto
@method_decorator(login_required, name="dispatch")
class ProductsListView(ListView):
    model = Products
    template_name = "products/products_list.html"
    context_object_name = "products"    


#Busqueda de productos y movimientos
@method_decorator(login_required, name="dispatch")
class CombinedSearchView(TemplateView):
    template_name = "products/search.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if query:
            # Solo buscar en productos y movimientos del usuario actual
            products_qs = Products.objects.filter(product=self.request.user)
            context['products'] = products_qs.filter(
                Q(product_name__icontains=query) |
                Q(category__icontains=query) |
                Q(supplier__icontains=query)
            ).distinct()

            movements_qs = StockMovement.objects.filter(product__product=self.request.user)
            # Evitar buscar texto en quantity (PositiveIntegerField) para evitar errores
            movement_filters = (
                Q(product__product_name__icontains=query) |
                Q(movement_type__icontains=query) |
                Q(notes__icontains=query)
            )
            if query.isdigit():
                movement_filters |= Q(quantity=int(query))

            context['movements'] = movements_qs.filter(movement_filters).distinct()
        else:
            context['products'] = Products.objects.none()
            context['movements'] = StockMovement.objects.none()
        return context


#Movimientos de stock
@method_decorator(login_required, name="dispatch")
class StockMovementCreateView(CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'movimientos/movement_add.html'
    success_url = reverse_lazy('movements_list')

    def form_valid(self, form):
        product = form.cleaned_data.get('product')
        quantity = form.cleaned_data.get('quantity')
        movement_type = form.cleaned_data.get('movement_type')
        
        if movement_type == 'OUT' and not self.stock_minimun(product.stock, quantity, product):
            return self.form_invalid(form)

        # Inyecta el usuario firmante antes de guardar el registro
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, ('movimiento realizado correctamente.'))
        return super().form_valid(form)


    def stock_minimun(self, stock, quantity, product):
        stock = product.stock
        quantity = quantity
        product = product
        if stock < quantity:
            messages.add_message(self.request, messages.ERROR, 'Stock insuficiente para %s. Disponible: %s, solicitado: %s' % (product.product_name, stock, quantity))
            return False
        elif quantity <= 2:
            messages.add_message(self.request, messages.WARNING, ('Stock en minimo de %s, por favor recargue stock.' % (product.product_name)))
            return True
        return True
        
    
#Lista de movimientos        
@method_decorator(login_required, name="dispatch")
class StockMovementListView(ListView):
    model = StockMovement
    template_name = 'movimientos/movement_list.html'
    context_object_name = 'movements'
    

class MovemenDeleteView(DeleteView):
    model = StockMovement
    template_name = "movimientos/movement_delete.html"
    success_url = reverse_lazy("movements_list")


    def get_queryset(self):
        return self.model.objects.filter(product__product=self.request.user)


    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Movimiento eliminado correctamente.')
        return super(MovemenDeleteView, self).form_valid(form)
    

    def get_success_url(self):
        return reverse('movements_list')


 #Exportar a csv
class CsvView(TemplateView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (f'attachment; filename=Productos.csv')
        writer = csv.writer(response)
        writer.writerow(['id', 'Nombre', 'Cantidad', 'Categoria', 'Proveedor', 'F-Entrada'])
        datos = Products.objects.all().values_list('id','product_name', 'stock', 'category', 'supplier', 'timestamp')
        for fila in datos:
            writer.writerow(fila)
        return response


def graphics_view(request):
    return render(request, 'general/graphics.html')