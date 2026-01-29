from django.contrib import admin
from .models import Doctor, DoctorSchedule, Appointment, AppointmentPayment, AppointmentReview


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'status', 'consultation_fee', 'rating', 'total_appointments', 'is_verified']
    list_filter = ['specialization', 'status', 'is_verified', 'created_at']
    search_fields = ['full_name', 'license_number', 'email']
    readonly_fields = ['total_appointments', 'rating', 'created_at', 'updated_at']


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'get_weekday_display', 'start_time', 'end_time', 'is_active']
    list_filter = ['weekday', 'is_active']
    search_fields = ['doctor__full_name']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'fee']
    list_filter = ['status', 'appointment_type', 'appointment_date', 'doctor__specialization']
    search_fields = ['patient__username', 'doctor__full_name', 'chief_complaint']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'completed_at']


@admin.register(AppointmentPayment)
class AppointmentPaymentAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'amount', 'payment_method', 'payment_status', 'paid_at']
    list_filter = ['payment_method', 'payment_status', 'created_at']
    search_fields = ['appointment__patient__username', 'transaction_id']


@admin.register(AppointmentReview)
class AppointmentReviewAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'doctor', 'patient', 'rating', 'would_recommend', 'created_at']
    list_filter = ['rating', 'would_recommend', 'created_at']
    search_fields = ['doctor__full_name', 'patient__username', 'review_text']