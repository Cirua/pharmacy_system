from django.contrib import admin
from .models import InventoryItem,  Sale

@admin.register(InventoryItem)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'selling_price', 'expiry_date')
    search_fields = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'inventory_item', 'quantity_sold', 'total_price', 'date')
    list_filter = ('date',)

