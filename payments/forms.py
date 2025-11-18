from django import forms
from .models import Coupon


class CouponForm(forms.ModelForm):
    """Form for creating/editing coupons"""
    
    class Meta:
        model = Coupon
        fields = [
            'code', 'description', 'coupon_type', 'value',
            'minimum_order_amount', 'maximum_discount',
            'usage_limit', 'usage_limit_per_user',
            'valid_from', 'valid_until', 'is_active',
            'applicable_categories', 'applicable_medicines'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'coupon_type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'minimum_order_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'maximum_discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'usage_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'usage_limit_per_user': forms.NumberInput(attrs={'class': 'form-control'}),
            'valid_from': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'valid_until': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'applicable_categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'applicable_medicines': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].required = True
        self.fields['coupon_type'].required = True
        self.fields['value'].required = True
        self.fields['valid_from'].required = True
        self.fields['valid_until'].required = True


class RefundRequestForm(forms.Form):
    """Form for refund requests"""
    
    REASON_CHOICES = [
        ('defective_product', 'Defective Product'),
        ('wrong_item', 'Wrong Item Delivered'),
        ('not_as_described', 'Product Not as Described'),
        ('changed_mind', 'Changed Mind'),
        ('duplicate_order', 'Duplicate Order'),
        ('other', 'Other'),
    ]
    
    reason = forms.ChoiceField(
        choices=REASON_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
