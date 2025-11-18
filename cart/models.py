from django.db import models
from django.conf import settings
from products.models import Medicine


class Cart(models.Model):
    """Shopping cart model"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user']
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def total_items(self):
        """Total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        """Total price of all items in cart"""
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Individual items in shopping cart"""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['cart', 'medicine']
    
    def __str__(self):
        return f"{self.quantity} x {self.medicine.name}"
    
    @property
    def total_price(self):
        """Total price for this cart item"""
        return self.medicine.current_price * self.quantity
    
    def clean(self):
        """Validate cart item"""
        from django.core.exceptions import ValidationError
        
        if self.quantity > self.medicine.max_order_quantity:
            raise ValidationError(
                f"Quantity cannot exceed {self.medicine.max_order_quantity} for this medicine."
            )
        
        if self.quantity < self.medicine.min_order_quantity:
            raise ValidationError(
                f"Minimum order quantity is {self.medicine.min_order_quantity} for this medicine."
            )
        
        if self.quantity > self.medicine.stock_quantity:
            raise ValidationError(
                f"Only {self.medicine.stock_quantity} items available in stock."
            )