from django.shortcuts import redirect
from django.urls import reverse

class AdminRedirectMiddleware:
    """
    Middleware to redirect admin users from Django admin to custom dashboard
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is trying to access Django admin (but not our custom admin pages)
        if (request.path.startswith('/admin/') and 
            not request.path.startswith('/admin/login/') and
            not request.path.startswith('/admin/medicines/') and
            not request.path.startswith('/admin/medicine/') and
            not request.path.startswith('/admin/categories/') and
            not request.path.startswith('/admin/category/') and
            not request.path.startswith('/admin/manufacturers/') and
            not request.path.startswith('/admin/manufacturer/')):
            
            if request.user.is_authenticated and (request.user.is_staff or getattr(request.user, 'user_type', None) == 'admin'):
                # Redirect to custom admin dashboard
                return redirect('doctor_appointments:admin_dashboard')
        
        response = self.get_response(request)
        return response