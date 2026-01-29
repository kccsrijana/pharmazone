from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import datetime


class Doctor(models.Model):
    """Doctor model for appointments"""
    SPECIALIZATION_CHOICES = [
        ('general', 'General Medicine'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('pediatrics', 'Pediatrics'),
        ('gynecology', 'Gynecology'),
        ('orthopedics', 'Orthopedics'),
        ('psychiatry', 'Psychiatry'),
        ('neurology', 'Neurology'),
        ('gastroenterology', 'Gastroenterology'),
        ('endocrinology', 'Endocrinology'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('on_leave', 'On Leave'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=100, unique=True)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('800.00'))
    profile_image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    bio = models.TextField(blank=True)
    hospital_affiliation = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('5.00'))
    total_appointments = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.full_name} - {self.get_specialization_display()}"
    
    def get_available_slots_for_date(self, date):
        """Get available time slots for a specific date"""
        weekday = date.weekday()
        
        # Get doctor's schedule for this weekday
        schedules = self.schedules.filter(weekday=weekday, is_active=True)
        
        available_slots = []
        for schedule in schedules:
            # Generate 30-minute slots
            current_time = datetime.datetime.combine(date, schedule.start_time)
            end_time = datetime.datetime.combine(date, schedule.end_time)
            
            while current_time < end_time:
                # Check if this slot is already booked
                is_booked = Appointment.objects.filter(
                    doctor=self,
                    appointment_date=date,
                    appointment_time=current_time.time(),
                    status__in=['confirmed', 'in_progress']
                ).exists()
                
                # Only add if not booked and in the future
                slot_datetime = timezone.make_aware(datetime.datetime.combine(date, current_time.time()))
                if not is_booked and slot_datetime > timezone.now():
                    available_slots.append({
                        'time': current_time.time(),
                        'display_time': current_time.strftime('%I:%M %p')
                    })
                
                current_time += datetime.timedelta(minutes=30)
        
        return available_slots


class DoctorSchedule(models.Model):
    """Doctor's weekly schedule"""
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['doctor', 'weekday', 'start_time']
        ordering = ['weekday', 'start_time']
    
    def __str__(self):
        return f"Dr. {self.doctor.full_name} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"


class Appointment(models.Model):
    """Patient appointment with doctor"""
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'General Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('routine_checkup', 'Routine Checkup'),
    ]
    
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    duration_minutes = models.PositiveIntegerField(default=30)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Patient information
    patient_age = models.PositiveIntegerField()
    patient_gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    chief_complaint = models.TextField()
    symptoms = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    
    # Appointment notes
    doctor_notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    prescription_notes = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        return f"Appointment: {self.patient.username} with Dr. {self.doctor.full_name} on {self.appointment_date} at {self.appointment_time}"
    
    @property
    def appointment_datetime(self):
        naive_dt = datetime.datetime.combine(self.appointment_date, self.appointment_time)
        return timezone.make_aware(naive_dt)
    
    @property
    def is_upcoming(self):
        return self.appointment_datetime > timezone.now() and self.status in ['pending', 'confirmed']
    
    @property
    def can_start(self):
        now = timezone.now()
        appointment_dt = self.appointment_datetime
        # Can start 10 minutes before scheduled time
        start_window = appointment_dt - datetime.timedelta(minutes=10)
        end_window = appointment_dt + datetime.timedelta(minutes=self.duration_minutes)
        return start_window <= now <= end_window and self.status == 'confirmed'


class AppointmentPayment(models.Model):
    """Payment for appointments"""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash Payment')], default='cash')
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')], default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment: Rs. {self.amount} for appointment {self.appointment.id}"


class AppointmentReview(models.Model):
    """Review and rating for appointments"""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='review')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment_reviews')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review_text = models.TextField(blank=True)
    would_recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review: {self.rating} stars for Dr. {self.doctor.full_name}"