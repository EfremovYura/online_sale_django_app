from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'model', 'release_date')
    list_filter = ('title', 'model', 'release_date')
    search_fields = ('title', 'model', 'release_date')
    ordering = ('title',)
