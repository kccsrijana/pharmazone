from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, OrderStatusHistory, ShippingAddress


class OrderItemInline(admin.TabularInline):
    """Inline for Order Items"""
    model = OrderItem
    extra = 0
    readonly_fields = ('medicine_name', 'medicine_strength', 'medicine_dosage_form', 'total_price')


class OrderStatusHistoryInline(admin.TabularInline):
    """Inline for Order Status History"""
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('changed_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order Admin"""
    
    list_display = (
        'order_number', 'user', 'status', 'payment_status', 
        'total_amount', 'requires_prescription', 'created_at'
    )
    list_filter = (
        'status', 'payment_status', 'requires_prescription', 
        'prescription_verified', 'created_at'
    )
    search_fields = (
        'order_number', 'user__username', 'user__email',
        'shipping_name', 'shipping_phone'
    )
    readonly_fields = (
        'order_number', 'created_at', 'updated_at', 'confirmed_at',
        'shipped_at', 'delivered_at'
    )
    
    fieldsets = (
        ('Order Information', {
            'fields': (
                'order_number', 'user', 'status', 'payment_status'
            )
        }),
        ('Pricing', {
            'fields': (
                'subtotal', 'tax_amount', 'shipping_cost', 
                'discount_amount', 'total_amount'
            )
        }),
        ('Shipping Information', {
            'fields': (
                'shipping_name', 'shipping_address', 'shipping_city',
                'shipping_state', 'shipping_postal_code', 'shipping_country',
                'shipping_phone'
            )
        }),
        ('Billing Information', {
            'fields': (
                'billing_name', 'billing_address', 'billing_city',
                'billing_state', 'billing_postal_code', 'billing_country'
            ),
            'classes': ('collapse',)
        }),
        ('Prescription', {
            'fields': (
                'requires_prescription', 'prescription_verified', 'prescription'
            )
        }),
        ('Notes', {
            'fields': ('notes', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': (
                'created_at', 'updated_at', 'confirmed_at',
                'shipped_at', 'delivered_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [OrderItemInline, OrderStatusHistoryInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Order Item Admin"""
    
    list_display = (
        'order', 'medicine', 'medicine_name', 'quantity', 
        'unit_price', 'total_price'
    )
    list_filter = ('order__created_at',)
    search_fields = (
        'order__order_number', 'medicine__name', 'medicine_name'
    )
    readonly_fields = (
        'medicine_name', 'medicine_strength', 'medicine_dosage_form', 'total_price'
    )


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    """Order Status History Admin"""
    
    list_display = ('order', 'status', 'changed_by', 'changed_at')
    list_filter = ('status', 'changed_at')
    search_fields = ('order__order_number', 'changed_by__username', 'notes')
    readonly_fields = ('changed_at',)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    """Shipping Address Admin"""
    
    list_display = ('user', 'name', 'city', 'state', 'is_default', 'created_at')
    list_filter = ('is_default', 'state', 'city', 'created_at')
    search_fields = ('user__username', 'name', 'address', 'city', 'state')
    readonly_fields = ('created_at',)