from django.db import models


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()

    def __str__(self):
        return self.name
    
class Sale(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT, default=1)
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.inventory_item.name} x{self.quantity_sold}"


