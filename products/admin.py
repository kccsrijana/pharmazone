from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Manufacturer, Medicine, MedicineReview, Prescription


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""
    
    list_display = ('name', 'slug', 'is_active', 'medicine_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    
    def medicine_count(self, obj):
        return obj.medicines.count()
    medicine_count.short_description = 'Medicines Count'


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """Manufacturer Admin"""
    
    list_display = ('name', 'country', 'website', 'medicine_count')
    list_filter = ('country',)
    search_fields = ('name', 'country', 'description')
    
    def medicine_count(self, obj):
        return obj.medicines.count()
    medicine_count.short_description = 'Medicines Count'


class MedicineReviewInline(admin.TabularInline):
    """Inline for Medicine Reviews"""
    model = MedicineReview
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """Medicine Admin"""
    
    list_display = (
        'name', 'generic_name', 'category', 'manufacturer', 'prescription_type',
        'strength', 'current_price', 'stock_quantity', 'is_active', 'is_featured'
    )
    list_filter = (
        'category', 'manufacturer', 'prescription_type', 'is_active', 
        'is_featured', 'requires_prescription', 'created_at'
    )
    search_fields = ('name', 'generic_name', 'composition', 'indications')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'current_price', 'discount_percentage')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'generic_name', 'description', 'category', 'manufacturer')
        }),
        ('Medicine Details', {
            'fields': (
                'prescription_type', 'dosage_form', 'strength', 'pack_size',
                'composition', 'indications', 'contraindications', 'side_effects',
                'storage_conditions', 'expiry_date'
            )
        }),
        ('Pricing & Inventory', {
            'fields': (
                'price', 'discount_price', 'current_price', 'discount_percentage',
                'stock_quantity', 'min_order_quantity', 'max_order_quantity'
            )
        }),
        ('Images', {
            'fields': ('image', 'additional_images')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'requires_prescription')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [MedicineReviewInline]
    
    def current_price(self, obj):
        return f"₹{obj.current_price}"
    current_price.short_description = 'Current Price'


@admin.register(MedicineReview)
class MedicineReviewAdmin(admin.ModelAdmin):
    """Medicine Review Admin"""
    
    list_display = ('medicine', 'user', 'rating', 'title', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('medicine__name', 'user__username', 'title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Review Information', {
            'fields': ('medicine', 'user', 'rating', 'title', 'comment')
        }),
        ('Verification', {
            'fields': ('is_verified_purchase',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    """Prescription Admin"""
    
    list_display = (
        'user', 'medicine', 'doctor_name', 'prescription_date', 
        'status', 'created_at'
    )
    list_filter = ('status', 'prescription_date', 'created_at')
    search_fields = (
        'user__username', 'medicine__name', 'doctor_name', 
        'doctor_license', 'notes'
    )
    readonly_fields = ('created_at', 'updated_at', 'prescription_image_preview')
    
    fieldsets = (
        ('Prescription Information', {
            'fields': (
                'user', 'medicine', 'prescription_image', 'prescription_image_preview',
                'doctor_name', 'doctor_license', 'prescription_date'
            )
        }),
        ('Review', {
            'fields': ('status', 'reviewed_by', 'review_notes', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def prescription_image_preview(self, obj):
        if obj.prescription_image:
            return format_html(
                '<img src="{}" width="200" height="200" style="border-radius: 5px;" />',
                obj.prescription_image.url
            )
        return "No image"
    prescription_image_preview.short_description = 'Image Preview'