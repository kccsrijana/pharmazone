from django.db import models
from django.conf import settings
from django.utils import timezone


class PharmacistChat(models.Model):
    """Chat conversation with pharmacist"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', 'General Question'),
        ('dosage', 'Dosage Information'),
        ('side_effects', 'Side Effects'),
        ('interactions', 'Drug Interactions'),
        ('prescription', 'Prescription Help'),
        ('symptoms', 'Symptom-based Recommendation'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pharmacist_chats')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    pharmacist = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_chats'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat #{self.id}: {self.subject} - {self.user.username}"
    
    @property
    def last_message(self):
        return self.messages.last()
    
    @property
    def unread_count_for_user(self):
        return self.messages.filter(is_from_pharmacist=True, is_read=False).count()
    
    @property
    def unread_count_for_pharmacist(self):
        return self.messages.filter(is_from_pharmacist=False, is_read=False).count()


class ChatMessage(models.Model):
    """Individual messages in a chat"""
    chat = models.ForeignKey(PharmacistChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_from_pharmacist = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        sender_type = "Pharmacist" if self.is_from_pharmacist else "Customer"
        return f"{sender_type}: {self.message[:50]}..."


class PharmacistProfile(models.Model):
    """Profile for pharmacists"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, unique=True)
    specialization = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pharmacist: {self.user.get_full_name() or self.user.username}"


class QuickResponse(models.Model):
    """Pre-defined quick responses for common questions"""
    CATEGORY_CHOICES = PharmacistChat.CATEGORY_CHOICES
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    question = models.CharField(max_length=200)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_category_display()}: {self.question}"