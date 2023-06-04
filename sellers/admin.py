from django.contrib import admin
from sellers.models import Seller


@admin.register(Seller)
class SellerModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller_type', 'email', 'country', 'city', 'street', 'house_number', 'provider',
                    'debt', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    fieldsets = (
        (None, {'fields': ('title', 'seller_type', 'provider', 'debt')}),
        ('Контактная информация', {'fields': ('email', 'country', 'city', 'street', 'house_number')}),
        ('Продукты', {'fields': ('products',)}),
        ('Даты', {'fields': ('created', 'updated')}),
    )
    search_fields = ('title', 'seller_type', 'email', 'country', 'city', 'street', 'house_number', 'products',
                     'provider', 'debt')
    list_filter = ('title', 'seller_type', 'email', 'country', 'city', 'street', 'house_number', 'provider',
                   'debt', 'created', 'updated')
    ordering = ('title', )
    actions = ['clear_debt', ]

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        queryset.update(debt=0.0)
