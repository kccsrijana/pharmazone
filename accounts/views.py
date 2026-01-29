from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, PharmacyProfileForm, CustomerProfileForm, UserUpdateForm, LoginForm
from .models import User, PharmacyProfile, CustomerProfile


def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('products:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            
            # Try to authenticate with username first
            user = authenticate(request, username=username, password=password)
            if user is None:
                # Try with email
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)  # Session expires when browser closes
                    
                    # Redirect based on user type with secure admin check
                    if user.user_type == 'pharmacy':
                        return redirect('accounts:pharmacy_dashboard')
                    elif (user.is_staff and 
                          (user.is_superuser or user.user_type == 'admin') and
                          user.username in ['admin']):  # Secure admin check
                        return redirect('doctor_appointments:admin_dashboard')
                    else:
                        return redirect('products:home')
                else:
                    messages.error(request, 'Your account is inactive. Please contact support.')
            else:
                messages.error(request, 'Invalid username/email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('products:home')


class SignUpView(CreateView):
    """User registration view"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        messages.success(
            self.request, 
            'Account created successfully! You can now login immediately.'
        )
        return response


@login_required
def profile_view(request):
    """User profile view"""
    user = request.user
    
    # Get or create profile based on user type
    if user.user_type == 'pharmacy':
        profile, created = PharmacyProfile.objects.get_or_create(user=user)
    elif user.user_type == 'customer':
        profile, created = CustomerProfile.objects.get_or_create(user=user)
    else:
        profile = None
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def update_profile(request):
    """Update user profile"""
    user = request.user
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        
        if user.user_type == 'pharmacy':
            profile, created = PharmacyProfile.objects.get_or_create(user=user)
            profile_form = PharmacyProfileForm(request.POST, instance=profile)
        elif user.user_type == 'customer':
            profile, created = CustomerProfile.objects.get_or_create(user=user)
            profile_form = CustomerProfileForm(request.POST, instance=profile)
        else:
            # For admin users and other types, no additional profile form needed
            profile_form = None
        
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            # Add form errors to messages for debugging
            if not user_form.is_valid():
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            if profile_form and not profile_form.is_valid():
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    else:
        user_form = UserUpdateForm(instance=user)
        
        if user.user_type == 'pharmacy':
            profile, created = PharmacyProfile.objects.get_or_create(user=user)
            profile_form = PharmacyProfileForm(instance=profile)
        elif user.user_type == 'customer':
            profile, created = CustomerProfile.objects.get_or_create(user=user)
            profile_form = CustomerProfileForm(instance=profile)
        else:
            # For admin users and other types, no additional profile form needed
            profile_form = None
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/update_profile.html', context)


@login_required
def pharmacy_dashboard(request):
    """Pharmacy dashboard view"""
    if request.user.user_type != 'pharmacy':
        messages.error(request, 'Access denied. This page is for pharmacy users only.')
        return redirect('home')
    
    pharmacy_profile = request.user.pharmacy_profile
    context = {
        'pharmacy_profile': pharmacy_profile,
    }
    return render(request, 'accounts/pharmacy_dashboard.html', context)


@login_required
def customer_dashboard(request):
    """Customer dashboard view"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Access denied. This page is for customer users only.')
        return redirect('home')
    
    customer_profile = request.user.customer_profile
    context = {
        'customer_profile': customer_profile,
    }
    return render(request, 'accounts/customer_dashboard.html', context)


@csrf_exempt
def check_username(request):
    """AJAX endpoint to check username availability"""
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'available': False})
        return JsonResponse({'available': True})
    return JsonResponse({'error': 'Invalid request'})


@csrf_exempt
def check_email(request):
    """AJAX endpoint to check email availability"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return JsonResponse({'available': False})
        return JsonResponse({'available': True})
    return JsonResponse({'error': 'Invalid request'})


@csrf_exempt
def validate_email_ajax(request):
    """AJAX endpoint for simple email validation"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        from .validators import EmailValidator
        result = EmailValidator.validate_simple(email)
        
        return JsonResponse({
            'is_valid': result['is_valid'],
            'errors': result['errors']
        })
    
    return JsonResponse({'error': 'Invalid request'})