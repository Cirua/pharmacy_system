from django.contrib import admin
from .models import InventoryItem, Supplier, Sale

@admin.register(InventoryItem)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'buying_price', 'selling_price', 'expiry_date')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'inventory_item', 'quantity_sold', 'total_price', 'date', 'sold_by')
    list_filter = ('date',)

