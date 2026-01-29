from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Custom user model for Pharmazone"""
    
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('pharmacy', 'Pharmacy'),
        ('admin', 'Admin'),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='customer'
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Nepal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class PharmacyProfile(models.Model):
    """Extended profile for pharmacy users"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmacy_profile')
    pharmacy_name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, unique=True)
    gst_number = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_approved = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_orders = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.pharmacy_name


class CustomerProfile(models.Model):
    """Extended profile for customer users"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    emergency_contact = models.CharField(max_length=15, blank=True)
    medical_conditions = models.TextField(blank=True, help_text="Any known medical conditions or allergies")
    preferred_pharmacy = models.ForeignKey(
        PharmacyProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_customers'
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"