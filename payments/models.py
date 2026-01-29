from django.db import models
from django.conf import settings
from orders.models import Order


class Payment(models.Model):
    """Payment model for order transactions"""
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
        ('wallet', 'Digital Wallet'),
        ('cod', 'Cash on Delivery'),
        ('esewa', 'eSewa'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Payment identification
    payment_id = models.CharField(max_length=100, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='NPR')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Gateway information
    gateway_transaction_id = models.CharField(max_length=200, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    gateway_name = models.CharField(max_length=50, default='esewa')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional information
    failure_reason = models.TextField(blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refund_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_id']),
            models.Index(fields=['order']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            import uuid
            self.payment_id = f"PAY_{str(uuid.uuid4())[:12].upper()}"
        super().save(*args, **kwargs)


class Invoice(models.Model):
    """Invoice model for completed orders"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Invoice identification
    invoice_number = models.CharField(max_length=50, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    
    # Invoice details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Company details (for invoice header)
    company_name = models.CharField(max_length=200, default='Pharmazone')
    company_address = models.TextField(default='Kathmandu, Nepal')
    company_phone = models.CharField(max_length=20, default='+977-1-4567890')
    company_email = models.EmailField(default='info@pharmazone.com.np')
    company_website = models.URLField(default='https://pharmazone.com.np')
    
    # Customer details (copied from order)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    
    # Additional information
    notes = models.TextField(blank=True)
    terms_and_conditions = models.TextField(
        default='Payment is due within 30 days. Thank you for your business!'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['order']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Invoice {self.invoice_number}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            from django.utils import timezone
            now = timezone.now()
            # Generate invoice number: INV-YYYY-MM-XXXXXX
            import uuid
            self.invoice_number = f"INV-{now.year}-{now.month:02d}-{str(uuid.uuid4())[:6].upper()}"
        
        # Copy customer details from order if not set
        if self.order and not self.customer_name:
            self.customer_name = self.order.shipping_name
            self.customer_email = self.order.user.email
            self.customer_phone = self.order.shipping_phone
            self.customer_address = f"{self.order.shipping_address}, {self.order.shipping_city}, {self.order.shipping_country}"
            
            # Copy amounts from order
            self.subtotal = self.order.subtotal
            self.tax_amount = self.order.tax_amount
            self.discount_amount = self.order.discount_amount
            self.shipping_amount = self.order.shipping_cost
            self.total_amount = self.order.total_amount
        
        super().save(*args, **kwargs)


class Refund(models.Model):
    """Refund model for processed refunds"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    refund_id = models.CharField(max_length=100, unique=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Gateway information
    gateway_refund_id = models.CharField(max_length=200, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Admin information
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_refunds'
    )
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refund {self.refund_id} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.refund_id:
            import uuid
            self.refund_id = f"REF_{str(uuid.uuid4())[:12].upper()}"
        super().save(*args, **kwargs)


class Coupon(models.Model):
    """Coupon/Discount codes"""
    
    COUPON_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Usage limits
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    usage_limit_per_user = models.PositiveIntegerField(default=1)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # Applicable categories/medicines
    applicable_categories = models.ManyToManyField(
        'products.Category',
        blank=True,
        related_name='coupons'
    )
    applicable_medicines = models.ManyToManyField(
        'products.Medicine',
        blank=True,
        related_name='coupons'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_coupons'
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Coupon: {self.code}"
    
    @property
    def is_valid(self):
        """Check if coupon is currently valid"""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (self.usage_limit is None or self.used_count < self.usage_limit)
        )
    
    def can_be_used_by_user(self, user):
        """Check if user can use this coupon"""
        from orders.models import Order
        user_usage_count = Order.objects.filter(
            user=user,
            payment__coupon=self
        ).count()
        return user_usage_count < self.usage_limit_per_user


class CouponUsage(models.Model):
    """Track coupon usage"""
    
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='coupon_usages'
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='coupon_usage')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['coupon', 'order']
        ordering = ['-used_at']
    
    def __str__(self):
        return f"{self.user.username} used {self.coupon.code} on Order {self.order.order_number}"