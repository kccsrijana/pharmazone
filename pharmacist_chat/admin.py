from django.contrib import admin
from .models import PharmacistChat, ChatMessage, PharmacistProfile, QuickResponse


@admin.register(PharmacistChat)
class PharmacistChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'category', 'status', 'pharmacist', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['user__username', 'subject', 'pharmacist__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'pharmacist')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender', 'is_from_pharmacist', 'is_read', 'created_at']
    list_filter = ['is_from_pharmacist', 'is_read', 'created_at']
    search_fields = ['chat__subject', 'sender__username', 'message']
    readonly_fields = ['created_at']


@admin.register(PharmacistProfile)
class PharmacistProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'license_number', 'experience_years', 'is_available', 'created_at']
    list_filter = ['is_available', 'experience_years', 'created_at']
    search_fields = ['user__username', 'license_number', 'specialization']
    readonly_fields = ['created_at']


@admin.register(QuickResponse)
class QuickResponseAdmin(admin.ModelAdmin):
    list_display = ['category', 'question', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['created_at']