from django import forms
from .models import Sale, InventoryItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InventoryForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'quantity', 'buying_price', 'selling_price', 'expiry_date']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['inventory_item', 'quantity_sold']
