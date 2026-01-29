from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Notification(models.Model):
    """In-app notifications for admin users"""
    
    NOTIFICATION_TYPES = [
        ('new_order', 'New Order'),
        ('payment_received', 'Payment Received'),
        ('prescription_order', 'Prescription Order'),
        ('low_stock', 'Low Stock Alert'),
        ('order_cancelled', 'Order Cancelled'),
        ('appointment_booked', 'Appointment Booked'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    
    # Related objects
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey('doctor_appointments.Appointment', on_delete=models.CASCADE, null=True, blank=True)
    medicine = models.ForeignKey('products.Medicine', on_delete=models.CASCADE, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_sent_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class EmailTemplate(models.Model):
    """Email templates for different notification types"""
    
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    html_content = models.TextField()
    text_content = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class NotificationSettings(models.Model):
    """User notification preferences"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    
    # Email notifications
    email_new_orders = models.BooleanField(default=True)
    email_payments = models.BooleanField(default=True)
    email_low_stock = models.BooleanField(default=True)
    email_appointments = models.BooleanField(default=True)
    
    # In-app notifications
    app_new_orders = models.BooleanField(default=True)
    app_payments = models.BooleanField(default=True)
    app_low_stock = models.BooleanField(default=True)
    app_appointments = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification settings for {self.user.username}"