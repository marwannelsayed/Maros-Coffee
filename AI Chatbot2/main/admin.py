from django.contrib import admin
from .models import Pizza, Size, Beverage, Order

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price')
    search_fields = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_multiplier')

@admin.register(Beverage)
class BeverageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pizza', 'size', 'beverage', 'total_price', 'created_at')
    list_filter = ('created_at',)
