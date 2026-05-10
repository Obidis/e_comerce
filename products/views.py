from django.db.models import Q
from django.views.generic import ListView
from products.models import Products



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
                
