from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from doctor_appointments.models import Doctor, DoctorSchedule
from decimal import Decimal
import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Add sample doctors with their weekly schedules'

    def handle(self, *args, **options):
        doctors_data = [
            {
                'username': 'dr_sharma_appt',
                'email': 'dr.sharma.appt@pharmazone.com',
                'password': 'doctor123',
                'full_name': 'Rajesh Sharma',
                'specialization': 'general',
                'license_number': 'NMC-APPT-001-2020',
                'qualification': 'MBBS, MD (General Medicine)',
                'experience_years': 15,
                'consultation_fee': Decimal('800.00'),
                'bio': 'Experienced general physician with 15 years of practice. Available for consultations Monday to Friday.',
                'hospital_affiliation': 'Tribhuvan University Teaching Hospital',
                'phone_number': '9841234567',
                'schedules': [
                    # Monday to Friday: 9 AM - 5 PM
                    {'weekday': 0, 'start_time': '09:00', 'end_time': '17:00'},  # Monday
                    {'weekday': 1, 'start_time': '09:00', 'end_time': '17:00'},  # Tuesday
                    {'weekday': 2, 'start_time': '09:00', 'end_time': '17:00'},  # Wednesday
                    {'weekday': 3, 'start_time': '09:00', 'end_time': '17:00'},  # Thursday
                    {'weekday': 4, 'start_time': '09:00', 'end_time': '17:00'},  # Friday
                ]
            },
            {
                'username': 'dr_patel_appt',
                'email': 'dr.patel.appt@pharmazone.com',
                'password': 'doctor123',
                'full_name': 'Sunita Patel',
                'specialization': 'cardiology',
                'license_number': 'NMC-APPT-002-2018',
                'qualification': 'MBBS, MD (Cardiology)',
                'experience_years': 12,
                'consultation_fee': Decimal('1200.00'),
                'bio': 'Cardiologist with expertise in heart disease. Available Tuesday to Saturday.',
                'hospital_affiliation': 'Shahid Gangalal National Heart Centre',
                'phone_number': '9841234568',
                'schedules': [
                    # Tuesday to Saturday: 10 AM - 6 PM
                    {'weekday': 1, 'start_time': '10:00', 'end_time': '18:00'},  # Tuesday
                    {'weekday': 2, 'start_time': '10:00', 'end_time': '18:00'},  # Wednesday
                    {'weekday': 3, 'start_time': '10:00', 'end_time': '18:00'},  # Thursday
                    {'weekday': 4, 'start_time': '10:00', 'end_time': '18:00'},  # Friday
                    {'weekday': 5, 'start_time': '10:00', 'end_time': '18:00'},  # Saturday
                ]
            },
            {
                'username': 'dr_thapa_appt',
                'email': 'dr.thapa.appt@pharmazone.com',
                'password': 'doctor123',
                'full_name': 'Amit Thapa',
                'specialization': 'dermatology',
                'license_number': 'NMC-APPT-003-2019',
                'qualification': 'MBBS, MD (Dermatology)',
                'experience_years': 8,
                'consultation_fee': Decimal('900.00'),
                'bio': 'Dermatologist specializing in skin conditions. Available Monday, Wednesday, Friday, and Sunday.',
                'hospital_affiliation': 'Nepal Medical College',
                'phone_number': '9841234569',
                'schedules': [
                    # Monday, Wednesday, Friday: 2 PM - 8 PM
                    {'weekday': 0, 'start_time': '14:00', 'end_time': '20:00'},  # Monday
                    {'weekday': 2, 'start_time': '14:00', 'end_time': '20:00'},  # Wednesday
                    {'weekday': 4, 'start_time': '14:00', 'end_time': '20:00'},  # Friday
                    # Sunday: 10 AM - 4 PM
                    {'weekday': 6, 'start_time': '10:00', 'end_time': '16:00'},  # Sunday
                ]
            },
            {
                'username': 'dr_gurung_appt',
                'email': 'dr.gurung.appt@pharmazone.com',
                'password': 'doctor123',
                'full_name': 'Maya Gurung',
                'specialization': 'pediatrics',
                'license_number': 'NMC-APPT-004-2017',
                'qualification': 'MBBS, MD (Pediatrics)',
                'experience_years': 10,
                'consultation_fee': Decimal('700.00'),
                'bio': 'Pediatrician dedicated to child health. Available Monday to Saturday mornings.',
                'hospital_affiliation': 'Kanti Children\'s Hospital',
                'phone_number': '9841234570',
                'schedules': [
                    # Monday to Saturday: 8 AM - 1 PM
                    {'weekday': 0, 'start_time': '08:00', 'end_time': '13:00'},  # Monday
                    {'weekday': 1, 'start_time': '08:00', 'end_time': '13:00'},  # Tuesday
                    {'weekday': 2, 'start_time': '08:00', 'end_time': '13:00'},  # Wednesday
                    {'weekday': 3, 'start_time': '08:00', 'end_time': '13:00'},  # Thursday
                    {'weekday': 4, 'start_time': '08:00', 'end_time': '13:00'},  # Friday
                    {'weekday': 5, 'start_time': '08:00', 'end_time': '13:00'},  # Saturday
                ]
            },
            {
                'username': 'dr_weekend',
                'email': 'dr.weekend@pharmazone.com',
                'password': 'doctor123',
                'full_name': 'Binod Shrestha',
                'specialization': 'orthopedics',
                'license_number': 'NMC-APPT-005-2016',
                'qualification': 'MBBS, MS (Orthopedics)',
                'experience_years': 14,
                'consultation_fee': Decimal('1000.00'),
                'bio': 'Orthopedic surgeon available on weekends for emergency consultations.',
                'hospital_affiliation': 'B&B Hospital',
                'phone_number': '9841234571',
                'schedules': [
                    # Saturday and Sunday: 9 AM - 5 PM
                    {'weekday': 5, 'start_time': '09:00', 'end_time': '17:00'},  # Saturday
                    {'weekday': 6, 'start_time': '09:00', 'end_time': '17:00'},  # Sunday
                ]
            },
        ]

        for doctor_data in doctors_data:
            # Create user account for doctor
            user, created = User.objects.get_or_create(
                username=doctor_data['username'],
                defaults={
                    'email': doctor_data['email'],
                    'first_name': doctor_data['full_name'].split()[0],
                    'last_name': ' '.join(doctor_data['full_name'].split()[1:]),
                    'is_staff': True,
                }
            )
            
            if created:
                user.set_password(doctor_data['password'])
                user.save()
                self.stdout.write(f"Created user account for {doctor_data['username']}")
            
            # Create doctor profile
            doctor, created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': doctor_data['full_name'],
                    'specialization': doctor_data['specialization'],
                    'license_number': doctor_data['license_number'],
                    'qualification': doctor_data['qualification'],
                    'experience_years': doctor_data['experience_years'],
                    'consultation_fee': doctor_data['consultation_fee'],
                    'bio': doctor_data['bio'],
                    'hospital_affiliation': doctor_data['hospital_affiliation'],
                    'phone_number': doctor_data['phone_number'],
                    'email': doctor_data['email'],
                    'is_verified': True,
                    'status': 'available',
                }
            )
            
            if created:
                self.stdout.write(f"Created doctor profile for Dr. {doctor_data['full_name']}")
                
                # Add schedules
                for schedule_data in doctor_data['schedules']:
                    start_time = datetime.datetime.strptime(schedule_data['start_time'], '%H:%M').time()
                    end_time = datetime.datetime.strptime(schedule_data['end_time'], '%H:%M').time()
                    
                    DoctorSchedule.objects.create(
                        doctor=doctor,
                        weekday=schedule_data['weekday'],
                        start_time=start_time,
                        end_time=end_time,
                        is_active=True
                    )
                
                self.stdout.write(f"Added {len(doctor_data['schedules'])} schedules for Dr. {doctor_data['full_name']}")
            else:
                self.stdout.write(f"Doctor profile already exists for Dr. {doctor_data['full_name']}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added {len(doctors_data)} doctors with their schedules!'
            )
        )
        
        # Display schedule summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write("DOCTOR AVAILABILITY SUMMARY:")
        self.stdout.write("="*50)
        
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for i, day in enumerate(weekdays):
            self.stdout.write(f"\n{day.upper()}:")
            day_schedules = DoctorSchedule.objects.filter(weekday=i, is_active=True)
            
            if day_schedules:
                for schedule in day_schedules:
                    self.stdout.write(f"  • Dr. {schedule.doctor.full_name} ({schedule.doctor.get_specialization_display()}) - {schedule.start_time.strftime('%I:%M %p')} to {schedule.end_time.strftime('%I:%M %p')}")
            else:
                self.stdout.write("  • No doctors available")
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write("You can now book appointments with these doctors!")
        self.stdout.write("Visit /appointments/ to see the booking system.")
        self.stdout.write("="*50)