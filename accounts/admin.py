from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, PharmacyProfile, CustomerProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'date_of_birth', 'address', 'city', 'country')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'email', 'first_name', 'last_name')
        }),
    )


@admin.register(PharmacyProfile)
class PharmacyProfileAdmin(admin.ModelAdmin):
    """Pharmacy Profile Admin"""
    
    list_display = ('pharmacy_name', 'user', 'license_number', 'is_approved', 'rating', 'total_orders')
    list_filter = ('is_approved',)
    search_fields = ('pharmacy_name', 'user__username', 'license_number', 'gst_number')
    readonly_fields = ('rating', 'total_orders')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'pharmacy_name', 'license_number', 'gst_number')
        }),
        ('Details', {
            'fields': ('description', 'website')
        }),
        ('Status & Statistics', {
            'fields': ('is_approved', 'rating', 'total_orders')
        }),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    """Customer Profile Admin"""
    
    list_display = ('user', 'emergency_contact', 'preferred_pharmacy')
    search_fields = ('user__username', 'user__email', 'emergency_contact')
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'emergency_contact', 'medical_conditions')
        }),
        ('Preferences', {
            'fields': ('preferred_pharmacy',)
        }),
    )