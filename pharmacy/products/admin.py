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

