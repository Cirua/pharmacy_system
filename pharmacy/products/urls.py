from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('inventory/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('records/', views.records, name='records'),
    path('sales/', views.sales, name='sales'),
    path('sales/new/', views.new_sale, name='new_sale'),
    path('logout/', views.logout_view, name='logout'),
]
