from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/add/', views.add_medicine, name='add_medicine'),
    path('inventory/edit/<int:pk>/', views.edit_medicine, name='edit_medicine'),
    path('sales/', views.sales, name='sales'),
    path('sales/new/', views.new_sale, name='new_sale'),
    path('logout/', views.logout_view, name='logout'),
]
