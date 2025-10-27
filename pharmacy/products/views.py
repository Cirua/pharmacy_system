from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Medicine, Sale
from .forms import MedicineForm, SaleForm
from django.contrib import messages
from django.utils import timezone

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'pharmacy/login.html', {'error': 'Invalid credentials'})
    return render(request, 'pharmacy/login.html')

@login_required
def home(request):
    low_stock = Medicine.objects.filter(quantity__lt=10)
    recent_sales = Sale.objects.order_by('-date')[:5]
    return render(request, 'pharmacy/home.html', {'low_stock': low_stock, 'recent_sales': recent_sales})

@login_required
def inventory(request):
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'pharmacy/inventory.html', {'medicines': medicines})

@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicine added.")
            return redirect('inventory')
    else:
        form = MedicineForm()
    return render(request, 'pharmacy/medicine_form.html', {'form': form})

@login_required
def edit_medicine(request, pk):
    med = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=med)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicine updated.")
            return redirect('inventory')
    else:
        form = MedicineForm(instance=med)
    return render(request, 'pharmacy/medicine_form.html', {'form': form, 'edit': True})

@login_required
def sales(request):
    sales = Sale.objects.order_by('-date')
    return render(request, 'pharmacy/sales.html', {'sales': sales})

@login_required
def new_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            med = sale.medicine
            qty = sale.quantity_sold
            if qty > med.quantity:
                messages.error(request, "Insufficient stock.")
                return redirect('new_sale')
            # compute total and update stock
            sale.total_price = qty * med.price
            sale.sold_by = request.user
            sale.date = timezone.now()
            med.quantity -= qty
            med.save()
            sale.save()
            messages.success(request, "Sale recorded.")
            return redirect('sales')
    else:
        form = SaleForm()
    return render(request, 'pharmacy/new_sale.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
