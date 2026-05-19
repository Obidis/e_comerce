
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import HomeView,  logout_view, login_view
from users.views import registro 
from products.views import CombinedSearchView, ProductsListView, ProductCreateView, ProductDeleteView, ProductUpdateView, StockMovementListView,StockMovementCreateView, CombinedCsvView, MovemenDeleteView, GraphicsView




urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', registro, name="register"),
    path('products/', ProductsListView.as_view(), name="products_list"),
    path('products/create/', ProductCreateView.as_view(), name="product_create"),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name="product_delete"),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name="product_update"),
    path('movements/', StockMovementListView.as_view(), name="movements_list"),
    path('movements/create/', StockMovementCreateView.as_view(), name="movements_create"),
    path('movements/delete/<int:pk>/', MovemenDeleteView.as_view(), name="movement_delete"),
    path('csv/', CombinedCsvView.as_view(), name="csv"),
    path('search/', CombinedSearchView.as_view(), name="search"),
    path('graficos/', GraphicsView.as_view(), name="graficos"),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
