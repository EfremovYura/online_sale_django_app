from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework import generics

from sellers.serializers import SellerSerializer, SellerUpdateSerializer
from sellers.models import Seller


class SellersCreateView(generics.CreateAPIView):
    serializer_class = SellerSerializer
    permission_classes = [IsAdminUser]


class SellersListView(generics.ListAPIView):
    serializer_class = SellerSerializer
    permission_classes = [IsAdminUser]
    queryset = Seller.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['country', 'city', 'seller_type']


class SellersDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SellerUpdateSerializer
    permission_classes = [IsAdminUser]
    queryset = Seller.objects.all()
