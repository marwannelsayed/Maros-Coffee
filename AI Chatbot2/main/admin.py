from django.contrib import admin
from .models import DrinkType, Customer, ChatMessage

@admin.register(DrinkType)
class DrinkTypeAdmin(admin.ModelAdmin):
    list_display = ('drink_type', 'price_small', 'price_medium', 'price_large', 'simple', 'double')
    search_fields = ('drink_type',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'session_key', 'created_at')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('customer', 'content', 'is_bot', 'timestamp')
    list_filter = ('is_bot', 'timestamp')
    search_fields = ('content',)
