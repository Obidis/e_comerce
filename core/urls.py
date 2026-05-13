
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import HomeView,  logout_view, login_view
from users.views import registro 
from products.views import SearchView, ProductsListView, ProductCreateView, ProductDeleteView, ProductUpdateView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', registro, name="register"),
    path('products/', ProductsListView.as_view(), name="products_list"),
    path('products/create/', ProductCreateView.as_view(), name="product_create"),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name="product_delete"),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name="product_update"),
    
    path('search/', SearchView.as_view(), name="search"),
  
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
