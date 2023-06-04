from products.serializers import ProductSerializer
from products.models import Product
from rest_framework.permissions import IsAdminUser
from rest_framework import generics


class ProductsCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductsListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()


class ProductsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
