from django.contrib import admin
from .models import Order, Customer, ChatMessage

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_price', 'created_at')
    list_filter = ('created_at',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'session_key', 'created_at')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('customer', 'content', 'is_bot', 'timestamp')
    list_filter = ('is_bot', 'timestamp')
    search_fields = ('content',)
