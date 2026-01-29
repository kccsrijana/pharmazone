from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, PharmacyProfile, CustomerProfile
from .validators import EmailValidator


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields"""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='customer'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        
        # Simple email validation
        validation_result = EmailValidator.validate_simple(email)
        if not validation_result['is_valid']:
            raise ValidationError(validation_result['errors'][0])
        
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone_number
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.user_type = self.cleaned_data['user_type']
        
        if commit:
            user.save()
            
            # Create appropriate profile based on user type
            if user.user_type == 'pharmacy':
                PharmacyProfile.objects.create(user=user)
            elif user.user_type == 'customer':
                CustomerProfile.objects.create(user=user)
        
        return user


class PharmacyProfileForm(forms.ModelForm):
    """Form for pharmacy profile completion"""
    
    class Meta:
        model = PharmacyProfile
        fields = [
            'pharmacy_name', 'license_number', 'gst_number', 
            'description', 'website'
        ]
        widgets = {
            'pharmacy_name': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
    
    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        # Exclude current instance when checking for duplicates
        existing_profiles = PharmacyProfile.objects.filter(license_number=license_number)
        if self.instance.pk:
            existing_profiles = existing_profiles.exclude(pk=self.instance.pk)
        
        if existing_profiles.exists():
            raise ValidationError("A pharmacy with this license number already exists.")
        return license_number


class CustomerProfileForm(forms.ModelForm):
    """Form for customer profile completion"""
    
    class Meta:
        model = CustomerProfile
        fields = [
            'emergency_contact', 'medical_conditions', 'preferred_pharmacy'
        ]
        widgets = {
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preferred_pharmacy': forms.Select(attrs={'class': 'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""
    
    COUNTRY_CHOICES = [
        ('Nepal', 'Nepal'),
        ('India', 'India'),
        ('Bangladesh', 'Bangladesh'),
        ('Pakistan', 'Pakistan'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Bhutan', 'Bhutan'),
        ('Maldives', 'Maldives'),
        ('Afghanistan', 'Afghanistan'),
        ('Myanmar', 'Myanmar'),
        ('Thailand', 'Thailand'),
        ('Other', 'Other'),
    ]
    
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        initial='Nepal',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'address', 'city', 'country'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone_number


class LoginForm(forms.Form):
    """Custom login form"""
    
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, initial=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['remember_me'].widget.attrs.update({
            'class': 'form-check-input'
        })
