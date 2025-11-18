from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline for Cart Items"""
    model = CartItem
    extra = 0
    readonly_fields = ('added_at', 'updated_at', 'total_price')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart Admin"""
    
    list_display = ('user', 'total_items', 'total_price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'total_items', 'total_price')
    
    fieldsets = (
        ('Cart Information', {
            'fields': ('user', 'total_items', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Cart Item Admin"""
    
    list_display = ('cart', 'medicine', 'quantity', 'total_price', 'added_at')
    list_filter = ('added_at', 'updated_at')
    search_fields = ('cart__user__username', 'medicine__name')
    readonly_fields = ('added_at', 'updated_at', 'total_price')
    
    fieldsets = (
        ('Item Information', {
            'fields': ('cart', 'medicine', 'quantity', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('added_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )