from django.urls import path
from sellers.views import SellersCreateView, SellersListView, SellersDetailView


urlpatterns = [
    path("create", SellersCreateView.as_view(), name='seller-create'),
    path("list", SellersListView.as_view(), name='seller-list'),
    path("<int:pk>", SellersDetailView.as_view(), name='seller'),
]
