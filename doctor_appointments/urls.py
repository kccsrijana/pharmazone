from django.urls import path
from . import views

app_name = 'doctor_appointments'

urlpatterns = [
    # Doctor listing and details
    path('', views.doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    
    # Appointment booking
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('get-slots/<int:doctor_id>/', views.get_available_slots, name='get_available_slots'),
    
    # Appointment management
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    
    # Reviews
    path('review/<int:appointment_id>/', views.review_appointment, name='review_appointment'),
    
    # Payment
    path('payment/<int:appointment_id>/', views.process_appointment_payment, name='process_appointment_payment'),
    
    # Admin appointment management
    path('admin/', views.admin_appointment_dashboard, name='admin_dashboard'),
    path('admin/simple/', views.admin_dashboard_simple, name='admin_dashboard_simple'),
    path('admin/test/', views.admin_test, name='admin_test'),
    path('admin/appointments/', views.admin_appointment_list, name='admin_appointment_list'),
    path('admin/appointment/<int:appointment_id>/', views.admin_appointment_detail, name='admin_appointment_detail'),
    path('admin/appointment/<int:appointment_id>/update-status/', views.admin_update_appointment_status, name='admin_update_appointment_status'),
    path('admin/appointment/<int:appointment_id>/reschedule/', views.admin_reschedule_appointment, name='admin_reschedule_appointment'),
]