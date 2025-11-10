from decimal import Decimal
from django.db.models import Sum
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
    
    
    featured_items = InventoryItem.objects.order_by('-id')[:4]
    return render(request, 'products/home.html', {'featured_items': featured_items})

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

def reports(request):
    """Display all sales reports."""
    sales = Sale.objects.order_by('-date')
    return render(request, 'products/reports.html', {'sales': sales})

def sales(request):
    inventory = InventoryItem.objects.all()
    sales = Sale.objects.order_by('-date')
    total_sales = Sale.objects.aggregate(total=Sum('total_price'))['total'] or 0
    return render(request, 'products/sales.html', {'inventory': inventory, 'sales': sales, 'total_sales': total_sales})


def add_to_cart(request, item_id):
    """Replaces the old new_sale function — handles sale recording from the product page."""
    item = get_object_or_404(InventoryItem, id=item_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity.")
            return redirect('sales')

        if quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
            return redirect('sales')

        if item.quantity < quantity:
            messages.error(request, f"Insufficient stock for {item.name}.")
            return redirect('sales')

        # Compute total and update stock
        total_price = Decimal(item.selling_price) * quantity
        item.quantity -= quantity
        item.save()

        # Save sale record
        Sale.objects.create(
            inventory_item=item,
            quantity_sold=quantity,
            total_price=total_price,
            date=timezone.now()
        )

        messages.success(request, f"Added {quantity} × {item.name} to Sales Report.")
        return redirect('sales')

    return redirect('sales')

def logout_view(request):
    logout(request)
    return redirect('login')
