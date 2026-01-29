from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from datetime import datetime, timedelta, date
from .models import Doctor, DoctorSchedule, Appointment, AppointmentPayment, AppointmentReview
from .forms import AppointmentBookingForm, AppointmentReviewForm
import json


def is_admin(user):
    """Check if user is admin - more secure check"""
    return (user.is_authenticated and 
            user.is_staff and 
            (user.is_superuser or user.user_type == 'admin') and
            user.username in ['admin'])  # Only allow specific admin usernames


@login_required
def process_appointment_payment(request, appointment_id):
    """Process payment for an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    if not hasattr(appointment, 'payment'):
        messages.error(request, 'Payment record not found for this appointment.')
        return redirect('doctor_appointments:appointment_detail', appointment_id=appointment.id)
    
    if appointment.payment.payment_status == 'paid':
        messages.info(request, 'This appointment has already been paid.')
        return redirect('doctor_appointments:appointment_detail', appointment_id=appointment.id)
    
    if request.method == 'POST':
        # Only cash payment is available
        appointment.payment.payment_method = 'cash'
        appointment.payment.payment_status = 'pending'
        appointment.payment.save()
        
        appointment.status = 'confirmed'
        appointment.confirmed_at = timezone.now()
        appointment.save()
        
        messages.success(request, 'Appointment confirmed! You can pay at the time of consultation.')
        return redirect('doctor_appointments:appointment_detail', appointment_id=appointment.id)
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'doctor_appointments/process_payment.html', context)
    context = {
        'appointment': appointment,
    }
    return render(request, 'doctor_appointments/process_payment.html', context)


def doctor_list(request):
    """List all available doctors with their schedules"""
    specialization = request.GET.get('specialization')
    search = request.GET.get('search')
    selected_date = request.GET.get('date')
    
    doctors = Doctor.objects.filter(is_verified=True, status='available')
    
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    if search:
        doctors = doctors.filter(
            Q(full_name__icontains=search) |
            Q(specialization__icontains=search) |
            Q(hospital_affiliation__icontains=search)
        )
    
    # If date is selected, filter doctors who have availability on that date
    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            weekday = selected_date_obj.weekday()
            
            # Get doctors who have schedules for this weekday
            doctors_with_schedule = DoctorSchedule.objects.filter(
                weekday=weekday,
                is_active=True
            ).values_list('doctor_id', flat=True)
            
            doctors = doctors.filter(id__in=doctors_with_schedule)
        except ValueError:
            selected_date = None
    
    # Add availability info for each doctor
    doctors_with_availability = []
    for doctor in doctors:
        doctor_info = {
            'doctor': doctor,
            'next_available': None,
            'available_today': False
        }
        
        # Check if doctor has availability today
        today = date.today()
        today_slots = doctor.get_available_slots_for_date(today)
        doctor_info['available_today'] = len(today_slots) > 0
        
        # Find next available date (within next 7 days)
        for i in range(7):
            check_date = today + timedelta(days=i)
            slots = doctor.get_available_slots_for_date(check_date)
            if slots:
                doctor_info['next_available'] = check_date
                break
        
        doctors_with_availability.append(doctor_info)
    
    # Get specializations for filter
    specializations = Doctor.SPECIALIZATION_CHOICES
    
    context = {
        'doctors_with_availability': doctors_with_availability,
        'specializations': specializations,
        'current_specialization': specialization,
        'search_query': search,
        'selected_date': selected_date,
        'today': date.today().isoformat(),
    }
    return render(request, 'doctor_appointments/doctor_list.html', context)


def doctor_detail(request, doctor_id):
    """Doctor profile and schedule view"""
    doctor = get_object_or_404(Doctor, id=doctor_id, is_verified=True)
    
    # Get doctor's reviews
    reviews = AppointmentReview.objects.filter(doctor=doctor).order_by('-created_at')[:5]
    
    # Get doctor's schedule for next 7 days
    today = date.today()
    weekly_schedule = []
    
    for i in range(7):
        check_date = today + timedelta(days=i)
        weekday = check_date.weekday()
        
        # Get schedule for this weekday
        day_schedules = DoctorSchedule.objects.filter(
            doctor=doctor,
            weekday=weekday,
            is_active=True
        ).order_by('start_time')
        
        # Get available slots
        available_slots = doctor.get_available_slots_for_date(check_date)
        
        weekly_schedule.append({
            'date': check_date,
            'date_str': check_date.strftime('%B %d, %Y'),
            'day_name': check_date.strftime('%A'),
            'is_today': check_date == today,
            'schedules': day_schedules,
            'available_slots': available_slots,
            'total_slots': len(available_slots)
        })
    
    context = {
        'doctor': doctor,
        'reviews': reviews,
        'weekly_schedule': weekly_schedule,
    }
    return render(request, 'doctor_appointments/doctor_detail.html', context)


@login_required
def book_appointment(request, doctor_id):
    """Book an appointment with a doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id, is_verified=True)
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST, doctor=doctor)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.fee = doctor.consultation_fee
            appointment.save()
            
            # Create payment record
            AppointmentPayment.objects.create(
                appointment=appointment,
                amount=doctor.consultation_fee,
                payment_method='cash'  # Only cash payment
            )
            
            messages.success(request, 'Appointment booked successfully! Please complete the payment.')
            return redirect('doctor_appointments:appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentBookingForm(doctor=doctor)
    
    # Get available dates (next 30 days)
    available_dates = []
    today = date.today()
    
    for i in range(30):
        check_date = today + timedelta(days=i)
        slots = doctor.get_available_slots_for_date(check_date)
        if slots:
            available_dates.append({
                'date': check_date,
                'date_str': check_date.strftime('%B %d, %Y (%A)'),
                'slot_count': len(slots)
            })
    
    context = {
        'doctor': doctor,
        'form': form,
        'available_dates': available_dates,
    }
    return render(request, 'doctor_appointments/book_appointment.html', context)


def get_available_slots(request, doctor_id):
    """AJAX endpoint to get available slots for a specific date"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    selected_date = request.GET.get('date')
    
    if not selected_date:
        return JsonResponse({'slots': []})
    
    try:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        slots = doctor.get_available_slots_for_date(date_obj)
        
        slot_data = []
        for slot in slots:
            slot_data.append({
                'value': slot['time'].strftime('%H:%M:%S'),
                'display': slot['display_time']
            })
        
        return JsonResponse({'slots': slot_data})
    except ValueError:
        return JsonResponse({'slots': []})


@login_required
def appointment_detail(request, appointment_id):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user has access to this appointment
    if appointment.patient != request.user and appointment.doctor.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('doctor_appointments:my_appointments')
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'doctor_appointments/appointment_detail.html', context)


@login_required
def my_appointments(request):
    """User's appointment history"""
    appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date', '-appointment_time')
    
    # Separate upcoming and past appointments
    now = timezone.now()
    upcoming = []
    past = []
    
    for appointment in appointments:
        appointment_dt = timezone.make_aware(datetime.combine(appointment.appointment_date, appointment.appointment_time))
        if appointment_dt > timezone.now() and appointment.status in ['pending', 'confirmed']:
            upcoming.append(appointment)
        else:
            past.append(appointment)
    
    context = {
        'upcoming_appointments': upcoming,
        'past_appointments': past,
    }
    return render(request, 'doctor_appointments/my_appointments.html', context)


@login_required
def cancel_appointment(request, appointment_id):
    """Cancel an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    # Can only cancel if appointment is in the future and not completed
    appointment_dt = timezone.make_aware(datetime.combine(appointment.appointment_date, appointment.appointment_time))
    if appointment_dt <= timezone.now() or appointment.status in ['completed', 'cancelled']:
        messages.error(request, 'This appointment cannot be cancelled.')
        return redirect('doctor_appointments:appointment_detail', appointment_id=appointment.id)
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('doctor_appointments:my_appointments')
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'doctor_appointments/cancel_appointment.html', context)


@login_required
def reschedule_appointment(request, appointment_id):
    """Reschedule an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    # Can only reschedule if appointment is in the future
    appointment_dt = timezone.make_aware(datetime.combine(appointment.appointment_date, appointment.appointment_time))
    if appointment_dt <= timezone.now() or appointment.status in ['completed', 'cancelled']:
        messages.error(request, 'This appointment cannot be rescheduled.')
        return redirect('doctor_appointments:appointment_detail', appointment_id=appointment.id)
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST, doctor=appointment.doctor, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment rescheduled successfully.')
            return redirect('doctor_appointments:appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentBookingForm(doctor=appointment.doctor, instance=appointment)
    
    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'doctor_appointments/reschedule_appointment.html', context)


@login_required
def review_appointment(request, appointment_id):
    """Review a completed appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user, status='completed')
    
    # Check if review already exists
    if hasattr(appointment, 'review'):
        messages.info(request, 'You have already reviewed this appointment.')
        return redirect('doctor_appointments:appointment_detail', appointment_id=appointment.id)
    
    if request.method == 'POST':
        form = AppointmentReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.appointment = appointment
            review.doctor = appointment.doctor
            review.patient = request.user
            review.save()
            
            # Update doctor's rating
            avg_rating = AppointmentReview.objects.filter(doctor=appointment.doctor).aggregate(
                avg_rating=Avg('rating')
            )['avg_rating']
            appointment.doctor.rating = round(avg_rating, 2) if avg_rating else 5.0
            appointment.doctor.save()
            
            messages.success(request, 'Thank you for your review!')
            return redirect('doctor_appointments:appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentReviewForm()
    
    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'doctor_appointments/review_appointment.html', context)


# Admin Appointment Management Views

@user_passes_test(is_admin)
def admin_appointment_list(request):
    """Admin view to list and manage all appointments"""
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    doctor_filter = request.GET.get('doctor', '')
    date_filter = request.GET.get('date', '')
    search = request.GET.get('search', '')
    
    # Base queryset
    appointments = Appointment.objects.select_related('patient', 'doctor', 'payment').all()
    
    # Apply filters
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    if doctor_filter:
        appointments = appointments.filter(doctor_id=doctor_filter)
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            appointments = appointments.filter(appointment_date=filter_date)
        except ValueError:
            pass
    
    if search:
        appointments = appointments.filter(
            Q(patient__username__icontains=search) |
            Q(patient__first_name__icontains=search) |
            Q(patient__last_name__icontains=search) |
            Q(doctor__full_name__icontains=search) |
            Q(chief_complaint__icontains=search)
        )
    
    # Order by date and time
    appointments = appointments.order_by('-appointment_date', '-appointment_time')
    
    # Pagination
    paginator = Paginator(appointments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get statistics
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    confirmed_appointments = Appointment.objects.filter(status='confirmed').count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    cancelled_appointments = Appointment.objects.filter(status='cancelled').count()
    
    # Get doctors for filter dropdown
    doctors = Doctor.objects.filter(is_verified=True).order_by('full_name')
    
    context = {
        'page_obj': page_obj,
        'appointments': page_obj,
        'doctors': doctors,
        'status_choices': Appointment.STATUS_CHOICES,
        'current_status': status_filter,
        'current_doctor': doctor_filter,
        'current_date': date_filter,
        'search_query': search,
        'stats': {
            'total': total_appointments,
            'pending': pending_appointments,
            'confirmed': confirmed_appointments,
            'completed': completed_appointments,
            'cancelled': cancelled_appointments,
        },
        'today': date.today().isoformat(),
    }
    return render(request, 'doctor_appointments/admin_appointment_list.html', context)


@user_passes_test(is_admin)
def admin_appointment_detail(request, appointment_id):
    """Admin view for appointment details with management options"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    context = {
        'appointment': appointment,
        'can_confirm': appointment.status == 'pending',
        'can_start': appointment.status == 'confirmed' and appointment.can_start,
        'can_complete': appointment.status in ['confirmed', 'in_progress'],
        'can_cancel': appointment.status in ['pending', 'confirmed'],
    }
    return render(request, 'doctor_appointments/admin_appointment_detail.html', context)


@user_passes_test(is_admin)
def admin_update_appointment_status(request, appointment_id):
    """Admin endpoint to update appointment status"""
    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return redirect('doctor_appointments:admin_appointment_detail', appointment_id=appointment_id)
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    new_status = request.POST.get('status')
    admin_notes = request.POST.get('admin_notes', '')
    
    if new_status not in dict(Appointment.STATUS_CHOICES):
        messages.error(request, 'Invalid status.')
        return redirect('doctor_appointments:admin_appointment_detail', appointment_id=appointment_id)
    
    old_status = appointment.status
    appointment.status = new_status
    
    # Update timestamps based on status
    if new_status == 'confirmed' and old_status == 'pending':
        appointment.confirmed_at = timezone.now()
        # Also update payment status if cash payment
        if hasattr(appointment, 'payment') and appointment.payment.payment_method == 'cash':
            appointment.payment.payment_status = 'pending'
            appointment.payment.save()
    elif new_status == 'completed':
        appointment.completed_at = timezone.now()
        # Mark payment as paid if cash
        if hasattr(appointment, 'payment') and appointment.payment.payment_method == 'cash':
            appointment.payment.payment_status = 'paid'
            appointment.payment.paid_at = timezone.now()
            appointment.payment.save()
    
    # Add admin notes to doctor notes
    if admin_notes:
        if appointment.doctor_notes:
            appointment.doctor_notes += f"\n\n[Admin Update - {timezone.now().strftime('%Y-%m-%d %H:%M')}]: {admin_notes}"
        else:
            appointment.doctor_notes = f"[Admin Update - {timezone.now().strftime('%Y-%m-%d %H:%M')}]: {admin_notes}"
    
    appointment.save()
    
    # Update doctor's total appointments count
    if new_status == 'completed':
        appointment.doctor.total_appointments += 1
        appointment.doctor.save()
    
    messages.success(request, f'Appointment status updated to {appointment.get_status_display()}.')
    return redirect('doctor_appointments:admin_appointment_detail', appointment_id=appointment_id)


@user_passes_test(is_admin)
def admin_reschedule_appointment(request, appointment_id):
    """Admin endpoint to reschedule an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Can only reschedule pending or confirmed appointments
    if appointment.status not in ['pending', 'confirmed']:
        messages.error(request, 'This appointment cannot be rescheduled.')
        return redirect('doctor_appointments:admin_appointment_detail', appointment_id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST, doctor=appointment.doctor, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment rescheduled successfully.')
            return redirect('doctor_appointments:admin_appointment_detail', appointment_id=appointment_id)
    else:
        form = AppointmentBookingForm(doctor=appointment.doctor, instance=appointment)
    
    # Get available dates (next 30 days)
    available_dates = []
    today = date.today()
    
    for i in range(30):
        check_date = today + timedelta(days=i)
        slots = appointment.doctor.get_available_slots_for_date(check_date)
        if slots:
            available_dates.append({
                'date': check_date,
                'date_str': check_date.strftime('%B %d, %Y (%A)'),
                'slot_count': len(slots)
            })
    
    context = {
        'appointment': appointment,
        'form': form,
        'available_dates': available_dates,
    }
    return render(request, 'doctor_appointments/admin_reschedule_appointment.html', context)


@user_passes_test(is_admin)
def admin_appointment_dashboard(request):
    """Comprehensive admin dashboard with all business metrics"""
    today = date.today()
    
    # === APPOINTMENT METRICS ===
    # Today's appointments
    todays_appointments = Appointment.objects.filter(appointment_date=today).order_by('appointment_time')
    
    # This week's appointments
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    weekly_appointments = Appointment.objects.filter(
        appointment_date__range=[week_start, week_end]
    ).count()
    
    # Monthly appointments
    month_start = today.replace(day=1)
    monthly_appointments = Appointment.objects.filter(
        appointment_date__gte=month_start
    ).count()
    
    # Appointment status statistics
    appointment_status_stats = {}
    for status_code, status_name in Appointment.STATUS_CHOICES:
        appointment_status_stats[status_code] = {
            'name': status_name,
            'count': Appointment.objects.filter(status=status_code).count()
        }
    
    # Upcoming pending appointments
    upcoming_pending = Appointment.objects.filter(
        status='pending',
        appointment_date__gte=today
    ).order_by('appointment_date', 'appointment_time')[:5]
    
    # === ORDER METRICS ===
    from orders.models import Order
    from decimal import Decimal
    
    # Today's orders
    todays_orders = Order.objects.filter(created_at__date=today)
    todays_revenue = sum(order.total_amount for order in todays_orders)
    
    # Weekly orders
    weekly_orders = Order.objects.filter(
        created_at__date__range=[week_start, week_end]
    )
    weekly_revenue = sum(order.total_amount for order in weekly_orders)
    
    # Monthly orders
    monthly_orders = Order.objects.filter(
        created_at__date__gte=month_start
    )
    monthly_revenue = sum(order.total_amount for order in monthly_orders)
    
    # Order status statistics
    order_status_stats = {}
    for status_code, status_name in Order.STATUS_CHOICES:
        order_status_stats[status_code] = {
            'name': status_name,
            'count': Order.objects.filter(status=status_code).count()
        }
    
    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    
    # === PAYMENT METRICS ===
    from payments.models import Payment, Invoice
    
    # Payment statistics (using 'status' field instead of 'payment_status')
    total_payments = Payment.objects.filter(status='completed').count()
    total_payment_amount = sum(
        payment.amount for payment in Payment.objects.filter(status='completed')
    )
    
    # Recent invoices
    recent_invoices = Invoice.objects.select_related('order').order_by('-created_at')[:5]
    
    # === USER METRICS ===
    from accounts.models import User
    
    # User statistics
    total_customers = User.objects.filter(user_type='customer').count()
    total_pharmacies = User.objects.filter(user_type='pharmacy').count()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    new_users_week = User.objects.filter(
        date_joined__date__range=[week_start, week_end]
    ).count()
    
    # === PRODUCT METRICS ===
    from products.models import Medicine, Category
    
    # Product statistics
    total_medicines = Medicine.objects.count()
    featured_medicines = Medicine.objects.filter(is_featured=True).count()
    total_categories = Category.objects.count()
    
    # === DOCTOR METRICS ===
    # Doctor statistics
    doctor_stats = Doctor.objects.annotate(
        appointment_count=Count('appointments'),
        pending_count=Count('appointments', filter=Q(appointments__status='pending')),
        confirmed_count=Count('appointments', filter=Q(appointments__status='confirmed'))
    ).order_by('-appointment_count')[:5]
    
    total_doctors = Doctor.objects.filter(is_verified=True).count()
    
    # === CHAT METRICS ===
    from pharmacist_chat.models import PharmacistChat
    
    # Chat statistics (using PharmacistChat model)
    total_chats = PharmacistChat.objects.count()
    active_chats = PharmacistChat.objects.filter(status='open').count()  # Using 'open' status instead of is_active
    todays_chats = PharmacistChat.objects.filter(created_at__date=today).count()
    
    context = {
        # Appointment data
        'todays_appointments': todays_appointments,
        'weekly_appointments': weekly_appointments,
        'monthly_appointments': monthly_appointments,
        'appointment_status_stats': appointment_status_stats,
        'upcoming_pending': upcoming_pending,
        
        # Order data
        'todays_orders_count': todays_orders.count(),
        'todays_revenue': todays_revenue,
        'weekly_orders_count': weekly_orders.count(),
        'weekly_revenue': weekly_revenue,
        'monthly_orders_count': monthly_orders.count(),
        'monthly_revenue': monthly_revenue,
        'order_status_stats': order_status_stats,
        'recent_orders': recent_orders,
        
        # Payment data
        'total_payments': total_payments,
        'total_payment_amount': total_payment_amount,
        'recent_invoices': recent_invoices,
        
        # User data
        'total_customers': total_customers,
        'total_pharmacies': total_pharmacies,
        'new_users_today': new_users_today,
        'new_users_week': new_users_week,
        
        # Product data
        'total_medicines': total_medicines,
        'featured_medicines': featured_medicines,
        'total_categories': total_categories,
        
        # Doctor data
        'doctor_stats': doctor_stats,
        'total_doctors': total_doctors,
        
        # Chat data
        'total_chats': total_chats,
        'active_chats': active_chats,
        'todays_chats': todays_chats,
        
        # General
        'today': today,
    }
    
    return render(request, 'doctor_appointments/admin_dashboard_working.html', context)


@user_passes_test(is_admin)
def admin_dashboard_simple(request):
    """Simple admin dashboard for debugging"""
    from datetime import date
    from orders.models import Order
    from accounts.models import User
    
    today = date.today()
    
    try:
        # Simple data collection
        todays_orders = Order.objects.filter(created_at__date=today)
        todays_revenue = sum(order.total_amount for order in todays_orders)
        total_customers = User.objects.filter(user_type='customer').count()
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
        todays_appointments = Appointment.objects.filter(appointment_date=today)
        
        context = {
            'todays_revenue': todays_revenue,
            'todays_orders_count': todays_orders.count(),
            'total_customers': total_customers,
            'today': today,
            'recent_orders': recent_orders,
            'todays_appointments': todays_appointments,
        }
        
    except Exception as e:
        context = {
            'error': str(e),
            'today': today,
        }
    
    return render(request, 'doctor_appointments/admin_dashboard_simple.html', context)


@user_passes_test(is_admin)
def admin_test(request):
    """Minimal test view"""
    from datetime import date
    from orders.models import Order
    from accounts.models import User
    
    context = {
        'today': date.today(),
        'total_customers': User.objects.filter(user_type='customer').count(),
        'todays_revenue': 1000,
    }
    
    return render(request, 'doctor_appointments/admin_test.html', context)