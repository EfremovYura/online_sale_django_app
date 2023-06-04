from django.urls import path
from products.views import ProductsListView, ProductsCreateView, ProductsDetailView


urlpatterns = [
    path("create", ProductsCreateView.as_view(), name='product-create'),
    path("list", ProductsListView.as_view(), name='product-list'),
    path("<int:pk>", ProductsDetailView.as_view(), name='product'),
]
