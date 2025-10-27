from django.db import models
from django.contrib.auth.models import User

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.medicine.name} x{self.quantity_sold}"
