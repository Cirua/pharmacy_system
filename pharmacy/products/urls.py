from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('products/home/', views.home, name='home'),
    path('products/inventory/', views.inventory, name='inventory'),
    path('products/inventory/add/', views.add_medicine, name='add_medicine'),
    path('products/inventory/edit/<int:pk>/', views.edit_medicine, name='edit_medicine'),
    path('products/sales/', views.sales, name='sales'),
    path('products/sales/new/', views.new_sale, name='new_sale'),
    path('products/logout/', views.logout_view, name='logout'),
]
