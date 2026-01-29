from django import forms
from .models import Order, ShippingAddress


class CheckoutForm(forms.ModelForm):
    """Form for checkout process"""
    
    class Meta:
        model = Order
        fields = [
            'shipping_name', 'shipping_address', 'shipping_city',
            'shipping_country', 'shipping_phone', 'notes'
        ]
        widgets = {
            'shipping_name': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_country': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shipping_name'].required = True
        self.fields['shipping_address'].required = True
        self.fields['shipping_city'].required = True
        self.fields['shipping_phone'].required = True
        
        # Set default values
        self.fields['shipping_country'].initial = 'Nepal'


class ShippingAddressForm(forms.ModelForm):
    """Form for shipping address"""
    
    class Meta:
        model = ShippingAddress
        fields = [
            'name', 'address', 'city', 'country', 'phone', 'is_default'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['address'].required = True
        self.fields['city'].required = True
        self.fields['phone'].required = True
        self.fields['country'].initial = 'Nepal'


class OrderStatusUpdateForm(forms.Form):
    """Form for updating order status"""
    
    status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
