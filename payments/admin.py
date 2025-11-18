from django.contrib import admin
from .models import Payment, Refund, Coupon, CouponUsage


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Payment Admin"""
    
    list_display = (
        'payment_id', 'order', 'user', 'amount', 'payment_method',
        'status', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'gateway_name', 'created_at')
    search_fields = (
        'payment_id', 'order__order_number', 'user__username',
        'gateway_transaction_id'
    )
    readonly_fields = (
        'payment_id', 'created_at', 'updated_at', 'completed_at',
        'gateway_response'
    )
    
    fieldsets = (
        ('Payment Information', {
            'fields': (
                'payment_id', 'order', 'user', 'amount', 'currency',
                'payment_method', 'status'
            )
        }),
        ('Gateway Information', {
            'fields': (
                'gateway_name', 'gateway_transaction_id', 'gateway_response'
            )
        }),
        ('Refund Information', {
            'fields': ('refund_amount', 'refund_reason'),
            'classes': ('collapse',)
        }),
        ('Failure Information', {
            'fields': ('failure_reason',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """Refund Admin"""
    
    list_display = (
        'refund_id', 'payment', 'amount', 'status', 'processed_by', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'refund_id', 'payment__payment_id', 'payment__order__order_number',
        'processed_by__username'
    )
    readonly_fields = (
        'refund_id', 'created_at', 'updated_at', 'completed_at',
        'gateway_response'
    )
    
    fieldsets = (
        ('Refund Information', {
            'fields': (
                'refund_id', 'payment', 'amount', 'reason', 'status'
            )
        }),
        ('Gateway Information', {
            'fields': ('gateway_refund_id', 'gateway_response')
        }),
        ('Processing', {
            'fields': ('processed_by', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Coupon Admin"""
    
    list_display = (
        'code', 'description', 'coupon_type', 'value', 'is_valid',
        'used_count', 'usage_limit', 'valid_until'
    )
    list_filter = (
        'coupon_type', 'is_active', 'valid_from', 'valid_until'
    )
    search_fields = ('code', 'description')
    readonly_fields = ('used_count', 'created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'code', 'description', 'coupon_type', 'value',
                'created_by', 'created_at'
            )
        }),
        ('Usage Limits', {
            'fields': (
                'minimum_order_amount', 'maximum_discount',
                'usage_limit', 'used_count', 'usage_limit_per_user'
            )
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until', 'is_active')
        }),
        ('Applicable Items', {
            'fields': ('applicable_categories', 'applicable_medicines'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    """Coupon Usage Admin"""
    
    list_display = (
        'coupon', 'user', 'order', 'discount_amount', 'used_at'
    )
    list_filter = ('used_at',)
    search_fields = (
        'coupon__code', 'user__username', 'order__order_number'
    )
    readonly_fields = ('used_at',)