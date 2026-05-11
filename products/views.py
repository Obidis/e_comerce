from django.db.models import Q
from django.views.generic import ListView
from products.models import Products
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from products.forms import ProductCreateForm
from django.urls import reverse_lazy
from django.contrib import messages




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
                Q(product_name__icontains=query) | Q(description__icontains=query)
            ).distinct()
        else:
            return Products.objects.none()
                
