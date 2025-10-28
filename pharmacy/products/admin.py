from django.contrib import admin
from .models import Medicine, Supplier, Sale

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'price', 'expiry_date')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'quantity_sold', 'total_price', 'date', 'sold_by')
    list_filter = ('date',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'quantity', 'buying_price', 'selling_price', 'expiry_date')
    list_filter = ('category', 'expiry_date')
    search_fields = ('name', 'category')
    ordering = ('name',)
