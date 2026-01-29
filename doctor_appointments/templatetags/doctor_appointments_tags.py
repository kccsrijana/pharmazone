from django import template
from doctor_appointments.models import Appointment

register = template.Library()

@register.simple_tag
def get_recent_appointments(limit=5):
    """Get recent appointments for debugging"""
    return Appointment.objects.all().order_by('-created_at')[:limit]