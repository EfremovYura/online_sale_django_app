from rest_framework import serializers
from sellers.models import Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"
        read_only_fields = ("id", "user", "created", "updated")


class SellerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"
        read_only_fields = ("id", "user", "created", "updated", "debt")
