from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse

@staff_member_required
def admin_redirect(request):
    """
    Redirect admin users to the modern custom dashboard instead of Django admin
    """
    if request.user.is_authenticated and (request.user.is_staff or request.user.user_type == 'admin'):
        # Redirect to your custom admin dashboard
        return redirect('doctor_appointments:admin_dashboard')
    else:
        # If not admin, redirect to home
        return redirect('products:home')