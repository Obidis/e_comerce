from django.db.models import Q
from django.views.generic import ListView
from products.models import Products, StockMovement
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, UpdateView
from products.forms import ProductCreateForm, StockMovementForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages



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
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(product=self.request.user)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Producto eliminado correctamente.')
        return super(ProductDeleteView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('home')
    
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
class ProductsListView(ListView):
    model = Products
    template_name = "products/products_list.html"
    context_object_name = "products"    


#buscador de productos
class SearchView(ListView):
    model = Products
    template_name = "products/search.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Products.objects.filter(
                Q(product_name__icontains=query) | Q(category__icontains=query) | Q(supplier__icontains=query)
            ).distinct()
        else:
            return Products.objects.none()
                
#MOvimientos de stock


@method_decorator(login_required, name="dispatch")
class StockMovementCreateView(CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'products/products_movement.html'
    success_url = reverse_lazy('movements_list')

    def form_valid(self, form):
        # Inyecta el usuario firmante antes de guardar el registro
        form.instance.user = self.request.user
        return super().form_valid(form)
    

@method_decorator(login_required, name="dispatch")
class StockMovementListView(ListView):
    model = StockMovement
    template_name = 'products/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 20

    def get_queryset(self):
        # Optimiza la consulta cargando relaciones externas en un solo query
        return StockMovement.objects.all().select_related('product', 'user')