from django import forms
from django.utils import timezone
from .models import Appointment, AppointmentReview
from datetime import datetime, date, timedelta


class AppointmentBookingForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': date.today().isoformat()}),
        help_text='Select your preferred appointment date'
    )
    
    appointment_time = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Available time slots will be shown based on selected date'
    )
    
    class Meta:
        model = Appointment
        fields = [
            'appointment_date', 'appointment_time', 'appointment_type', 
            'patient_age', 'patient_gender', 'chief_complaint', 'symptoms', 
            'medical_history', 'current_medications', 'allergies'
        ]
        widgets = {
            'appointment_type': forms.Select(attrs={'class': 'form-select'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 120}),
            'patient_gender': forms.Select(attrs={'class': 'form-select'}),
            'chief_complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your main health concern'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your current symptoms (optional)'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any previous medical conditions or surgeries (optional)'}),
            'current_medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List any medications you are currently taking (optional)'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any known allergies (optional)'}),
        }
        labels = {
            'appointment_type': 'Type of Appointment',
            'patient_age': 'Your Age',
            'patient_gender': 'Gender',
            'chief_complaint': 'Main Health Concern',
            'symptoms': 'Current Symptoms',
            'medical_history': 'Medical History',
            'current_medications': 'Current Medications',
            'allergies': 'Allergies',
        }
    
    def __init__(self, *args, **kwargs):
        self.doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        
        # Set minimum date to today
        self.fields['appointment_date'].widget.attrs['min'] = date.today().isoformat()
        
        # If doctor is provided and date is selected, populate time slots
        if self.doctor and self.data.get('appointment_date'):
            try:
                selected_date = datetime.strptime(self.data['appointment_date'], '%Y-%m-%d').date()
                available_slots = self.doctor.get_available_slots_for_date(selected_date)
                
                time_choices = [('', 'Select a time slot')]
                for slot in available_slots:
                    time_choices.append((slot['time'].strftime('%H:%M:%S'), slot['display_time']))
                
                self.fields['appointment_time'].choices = time_choices
            except (ValueError, TypeError):
                self.fields['appointment_time'].choices = [('', 'Please select a valid date first')]
        else:
            self.fields['appointment_time'].choices = [('', 'Please select a date first')]
    
    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date < date.today():
            raise forms.ValidationError('Appointment date cannot be in the past.')
        
        # Don't allow appointments more than 30 days in advance
        max_date = date.today() + timedelta(days=30)
        if appointment_date > max_date:
            raise forms.ValidationError('Appointments can only be booked up to 30 days in advance.')
        
        return appointment_date
    
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        
        if appointment_date and appointment_time and self.doctor:
            # Convert time string back to time object
            if isinstance(appointment_time, str):
                try:
                    appointment_time = datetime.strptime(appointment_time, '%H:%M:%S').time()
                except ValueError:
                    raise forms.ValidationError('Invalid time format.')
            
            # Check if the slot is still available
            appointment_datetime = timezone.make_aware(datetime.combine(appointment_date, appointment_time))
            if appointment_datetime <= timezone.now():
                raise forms.ValidationError('Selected appointment time has passed.')
            
            # Check if slot is already booked
            existing_appointment = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['pending', 'confirmed', 'in_progress']
            ).exists()
            
            if existing_appointment:
                raise forms.ValidationError('This time slot is no longer available. Please select another time.')
        
        return cleaned_data


class AppointmentReviewForm(forms.ModelForm):
    class Meta:
        model = AppointmentReview
        fields = ['rating', 'review_text', 'would_recommend']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this doctor...'
            }),
            'would_recommend': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'rating': 'Overall Rating',
            'review_text': 'Your Review',
            'would_recommend': 'Would you recommend this doctor?',
        }