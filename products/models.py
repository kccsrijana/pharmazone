from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from accounts.models import PharmacyProfile


class Category(models.Model):
    """Medicine categories"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """Medicine manufacturers"""
    
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='manufacturers/', blank=True, null=True)
    
    def __str__(self):
        return self.name


class Medicine(models.Model):
    """Medicine/Product model"""
    
    PRESCRIPTION_CHOICES = [
        ('otc', 'Over the Counter'),
        ('prescription', 'Prescription Required'),
        ('controlled', 'Controlled Substance'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    generic_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='medicines')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='medicines')
    prescription_type = models.CharField(max_length=20, choices=PRESCRIPTION_CHOICES, default='otc')
    
    # Medicine specific fields
    dosage_form = models.CharField(max_length=100, blank=True)  # tablet, syrup, injection, etc.
    strength = models.CharField(max_length=100, blank=True)  # 500mg, 10ml, etc.
    pack_size = models.CharField(max_length=50, blank=True)  # 10 tablets, 100ml, etc.
    composition = models.TextField(blank=True)
    indications = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    storage_conditions = models.TextField(blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    # Pricing and inventory
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    min_order_quantity = models.PositiveIntegerField(default=1)
    max_order_quantity = models.PositiveIntegerField(default=100)
    
    # Images
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)
    additional_images = models.JSONField(default=list, blank=True)
    
    # Status and metadata
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    requires_prescription = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['prescription_type']),
            models.Index(fields=['is_active']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.strength}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.strength})"
    
    @property
    def current_price(self):
        """Return the current price (discount price if available, otherwise regular price)"""
        return self.discount_price if self.discount_price else self.price
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.discount_price and self.price:
            return round(((self.price - self.discount_price) / self.price) * 100, 2)
        return 0
    
    @property
    def is_in_stock(self):
        """Check if medicine is in stock"""
        return self.stock_quantity > 0


class MedicineReview(models.Model):
    """Customer reviews for medicines"""
    
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='medicine_reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['medicine', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s review for {self.medicine.name}"


class Prescription(models.Model):
    """Prescription uploads for prescription medicines"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prescriptions')
    prescription_image = models.ImageField(upload_to='prescriptions/')
    doctor_name = models.CharField(max_length=200)
    doctor_license = models.CharField(max_length=100, blank=True)
    prescription_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_prescriptions'
    )
    review_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prescription for {self.medicine.name} by {self.user.username}"