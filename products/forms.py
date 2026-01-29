from django import forms
from .models import MedicineReview, Prescription, Medicine, Category, Manufacturer


class MedicineReviewForm(forms.ModelForm):
    """Form for medicine reviews"""
    
    class Meta:
        model = MedicineReview
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].required = True
        self.fields['title'].required = True
        self.fields['comment'].required = True


class PrescriptionUploadForm(forms.ModelForm):
    """Form for prescription uploads"""
    
    class Meta:
        model = Prescription
        fields = [
            'medicine', 'prescription_image', 'doctor_name', 
            'doctor_license', 'prescription_date', 'notes'
        ]
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'prescription_image': forms.FileInput(attrs={'class': 'form-control'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'doctor_license': forms.TextInput(attrs={'class': 'form-control'}),
            'prescription_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show prescription medicines
        self.fields['medicine'].queryset = Medicine.objects.filter(
            prescription_type__in=['prescription', 'controlled'],
            is_active=True
        )
        self.fields['medicine'].required = True
        self.fields['prescription_image'].required = True
        self.fields['doctor_name'].required = True
        self.fields['prescription_date'].required = True


class AdminMedicineForm(forms.ModelForm):
    """Admin form for managing medicines"""
    
    class Meta:
        model = Medicine
        fields = [
            'name', 'generic_name', 'description', 'category', 'manufacturer',
            'prescription_type', 'dosage_form', 'strength', 'pack_size',
            'composition', 'indications', 'contraindications', 'side_effects',
            'storage_conditions', 'expiry_date', 'price', 'discount_price',
            'stock_quantity', 'min_order_quantity', 'max_order_quantity',
            'image', 'is_active', 'is_featured', 'requires_prescription'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'manufacturer': forms.Select(attrs={'class': 'form-control'}),
            'prescription_type': forms.Select(attrs={'class': 'form-control'}),
            'dosage_form': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Tablet, Syrup, Injection'}),
            'strength': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg, 10ml'}),
            'pack_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 10 tablets, 100ml'}),
            'composition': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'indications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contraindications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'side_effects': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'storage_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'min_order_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'max_order_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requires_prescription': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['description'].required = True
        self.fields['category'].required = True
        self.fields['manufacturer'].required = True
        self.fields['price'].required = True
        self.fields['stock_quantity'].required = True
        
        # Set default values
        if not self.instance.pk:
            self.fields['is_active'].initial = True
            self.fields['min_order_quantity'].initial = 1
            self.fields['max_order_quantity'].initial = 100
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')
        min_order = cleaned_data.get('min_order_quantity')
        max_order = cleaned_data.get('max_order_quantity')
        
        # Validate discount price
        if discount_price and price and discount_price >= price:
            raise forms.ValidationError('Discount price must be less than regular price.')
        
        # Validate order quantities
        if min_order and max_order and min_order > max_order:
            raise forms.ValidationError('Minimum order quantity cannot be greater than maximum order quantity.')
        
        return cleaned_data


class CategoryForm(forms.ModelForm):
    """Form for managing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        if not self.instance.pk:
            self.fields['is_active'].initial = True


class ManufacturerForm(forms.ModelForm):
    """Form for managing manufacturers"""
    
    class Meta:
        model = Manufacturer
        fields = ['name', 'country', 'website', 'description', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['country'].required = True
