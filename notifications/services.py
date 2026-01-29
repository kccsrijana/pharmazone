from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from .models import Notification, NotificationSettings, EmailTemplate
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class NotificationService:
    """Service for handling all types of notifications"""
    
    @staticmethod
    def create_notification(recipient, notification_type, title, message, priority='medium', 
                          order=None, appointment=None, medicine=None):
        """Create an in-app notification"""
        try:
            notification = Notification.objects.create(
                recipient=recipient,
                notification_type=notification_type,
                title=title,
                message=message,
                priority=priority,
                order=order,
                appointment=appointment,
                medicine=medicine
            )
            return notification
        except Exception as e:
            logger.error(f"Failed to create notification: {e}")
            return None
    
    @staticmethod
    def send_email_notification(recipient_email, subject, template_name, context):
        """Send email notification using template"""
        try:
            html_message = render_to_string(f'notifications/emails/{template_name}.html', context)
            text_message = render_to_string(f'notifications/emails/{template_name}.txt', context)
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return False
    
    @staticmethod
    def notify_new_order(order):
        """Send notifications for new order"""
        # Get all admin users
        admin_users = User.objects.filter(
            models.Q(is_staff=True) | models.Q(user_type='admin')
        )
        
        for admin in admin_users:
            # Check user preferences
            settings_obj, created = NotificationSettings.objects.get_or_create(user=admin)
            
            # Create in-app notification
            if settings_obj.app_new_orders:
                NotificationService.create_notification(
                    recipient=admin,
                    notification_type='new_order',
                    title=f'New Order #{order.id}',
                    message=f'New order from {order.user.username} for Rs. {order.total_amount}',
                    priority='high',
                    order=order
                )
            
            # Send email notification
            if settings_obj.email_new_orders:
                context = {
                    'order': order,
                    'admin': admin,
                    'site_name': 'Pharmazone'
                }
                NotificationService.send_email_notification(
                    recipient_email=admin.email,
                    subject=f'New Order #{order.id} - Pharmazone',
                    template_name='new_order_admin',
                    context=context
                )
        
        # Send confirmation email to customer
        if order.user.email:
            context = {
                'order': order,
                'customer': order.user,
                'site_name': 'Pharmazone'
            }
            NotificationService.send_email_notification(
                recipient_email=order.user.email,
                subject=f'Order Confirmation #{order.id} - Pharmazone',
                template_name='order_confirmation_customer',
                context=context
            )
    
    @staticmethod
    def notify_payment_received(order):
        """Send notifications for payment received"""
        admin_users = User.objects.filter(
            models.Q(is_staff=True) | models.Q(user_type='admin')
        )
        
        for admin in admin_users:
            settings_obj, created = NotificationSettings.objects.get_or_create(user=admin)
            
            if settings_obj.app_payments:
                NotificationService.create_notification(
                    recipient=admin,
                    notification_type='payment_received',
                    title=f'Payment Received - Order #{order.id}',
                    message=f'Payment of Rs. {order.total_amount} received for order #{order.id}',
                    priority='medium',
                    order=order
                )
        
        # Send payment confirmation to customer
        if order.user.email:
            context = {
                'order': order,
                'customer': order.user,
                'site_name': 'Pharmazone'
            }
            NotificationService.send_email_notification(
                recipient_email=order.user.email,
                subject=f'Payment Confirmed - Order #{order.id} - Pharmazone',
                template_name='payment_confirmation_customer',
                context=context
            )
    
    @staticmethod
    def notify_prescription_order(order):
        """Send notifications for prescription orders"""
        admin_users = User.objects.filter(
            models.Q(is_staff=True) | models.Q(user_type='admin')
        )
        
        for admin in admin_users:
            settings_obj, created = NotificationSettings.objects.get_or_create(user=admin)
            
            if settings_obj.app_new_orders:
                NotificationService.create_notification(
                    recipient=admin,
                    notification_type='prescription_order',
                    title=f'Prescription Order #{order.id}',
                    message=f'New prescription order requires review - Order #{order.id}',
                    priority='urgent',
                    order=order
                )
    
    @staticmethod
    def notify_low_stock(medicine):
        """Send notifications for low stock"""
        admin_users = User.objects.filter(
            models.Q(is_staff=True) | models.Q(user_type='admin')
        )
        
        for admin in admin_users:
            settings_obj, created = NotificationSettings.objects.get_or_create(user=admin)
            
            if settings_obj.app_low_stock:
                NotificationService.create_notification(
                    recipient=admin,
                    notification_type='low_stock',
                    title=f'Low Stock Alert - {medicine.name}',
                    message=f'{medicine.name} is running low (Only {medicine.stock_quantity} left)',
                    priority='high',
                    medicine=medicine
                )
    
    @staticmethod
    def notify_appointment_booked(appointment):
        """Send notifications for new appointments"""
        admin_users = User.objects.filter(
            models.Q(is_staff=True) | models.Q(user_type='admin')
        )
        
        for admin in admin_users:
            settings_obj, created = NotificationSettings.objects.get_or_create(user=admin)
            
            if settings_obj.app_appointments:
                NotificationService.create_notification(
                    recipient=admin,
                    notification_type='appointment_booked',
                    title=f'New Appointment Booked',
                    message=f'New appointment with Dr. {appointment.doctor.name} on {appointment.appointment_date}',
                    priority='medium',
                    appointment=appointment
                )
    
    @staticmethod
    def get_unread_count(user):
        """Get count of unread notifications for user"""
        return Notification.objects.filter(recipient=user, is_read=False).count()
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for user"""
        Notification.objects.filter(recipient=user, is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )