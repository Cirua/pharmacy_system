from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import InventoryItem, Sale
from .forms import InventoryForm, SaleForm, SignUpForm
from django.contrib import messages
from django.utils import timezone


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'products/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'products/login.html', {'error': 'Invalid credentials'})
    return render(request, 'products/login.html')


@login_required
def home(request):
    low_stock = InventoryItem.objects.filter(quantity__lt=10)
    recent_sales = Sale.objects.order_by('-date')[:5]
    return render(request, 'products/home.html', {'low_stock': low_stock, 'recent_sales': recent_sales})

def inventory(request):
    """Display all inventory items and handle adding new ones."""
    items = InventoryItem.objects.all().order_by('name')
    
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully!")
            return redirect('inventory')
    else:
        form = InventoryForm()
    
    return render(request, 'products/inventory.html', {
        'form': form,
        'items': items,
    })


def edit_item(request, item_id):
    """Edit an existing inventory item."""
    item = get_object_or_404(InventoryItem, id=item_id)
    
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully!")
            return redirect('inventory')
    else:
        form = InventoryForm(instance=item)
    
    return render(request, 'products/inventory.html', {
        'form': form,
        'items': InventoryItem.objects.all(),
        'edit_mode': True,
        'edit_item': item
    })


def delete_item(request, item_id):
    """Delete an item from inventory."""
    item = get_object_or_404(InventoryItem, id=item_id)
    item.delete()
    messages.success(request, "Item deleted successfully!")
    return redirect('inventory')

def records(request):
    """Display all inventory (stock) records."""
    items = InventoryItem.objects.all().order_by('name')
    return render(request, 'products/records.html', {'items': items})

def sales(request):
    sales = Sale.objects.order_by('-date')
    return render(request, 'products/sales.html', {'sales': sales})


def new_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            inventory = sale.inventory_item
            qty = sale.quantity_sold
            if qty > inventory.quantity:
                messages.error(request, "Insufficient stock.")
                return redirect('new_sale')
            # compute total and update stock
            sale.total_price = qty * inventory.selling_price
            sale.sold_by = request.user
            sale.date = timezone.now()
            inventory.quantity -= qty
            inventory.save()
            sale.save()
            messages.success(request, "Sale recorded.")
            return redirect('sales')
    else:
        form = SaleForm()
    return render(request, 'products/new_sale.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
