from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from accounts.models import User, CustomerProfile


class Command(BaseCommand):
    help = 'Create demo customer accounts for testing'

    def handle(self, *args, **options):
        demo_customers = [
            {
                'username': 'demo_customer1',
                'email': 'customer1@demo.com',
                'password': 'demo123',
                'first_name': 'Rajesh',
                'last_name': 'Sharma',
                'phone_number': '+977-9841234567',
                'address': 'Thamel, Kathmandu',
                'city': 'Kathmandu',
                'country': 'Nepal',
            },
            {
                'username': 'demo_customer2',
                'email': 'customer2@demo.com',
                'password': 'demo123',
                'first_name': 'Sita',
                'last_name': 'Poudel',
                'phone_number': '+977-9851234567',
                'address': 'Patan Dhoka, Lalitpur',
                'city': 'Lalitpur',
                'country': 'Nepal',
            },
            {
                'username': 'demo_customer3',
                'email': 'customer3@demo.com',
                'password': 'demo123',
                'first_name': 'Arjun',
                'last_name': 'Thapa',
                'phone_number': '+977-9861234567',
                'address': 'Bhaktapur Durbar Square',
                'city': 'Bhaktapur',
                'country': 'Nepal',
            },
            {
                'username': 'demo_customer4',
                'email': 'customer4@demo.com',
                'password': 'demo123',
                'first_name': 'Maya',
                'last_name': 'Gurung',
                'phone_number': '+977-9871234567',
                'address': 'Lakeside, Pokhara',
                'city': 'Pokhara',
                'country': 'Nepal',
            },
            {
                'username': 'demo_customer5',
                'email': 'customer5@demo.com',
                'password': 'demo123',
                'first_name': 'Bikash',
                'last_name': 'Rai',
                'phone_number': '+977-9881234567',
                'address': 'Biratnagar Main Road',
                'city': 'Biratnagar',
                'country': 'Nepal',
            }
        ]

        created_count = 0
        updated_count = 0

        for customer_data in demo_customers:
            username = customer_data['username']
            
            # Check if user already exists
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': customer_data['email'],
                    'password': make_password(customer_data['password']),
                    'first_name': customer_data['first_name'],
                    'last_name': customer_data['last_name'],
                    'phone_number': customer_data['phone_number'],
                    'address': customer_data['address'],
                    'city': customer_data['city'],
                    'country': customer_data['country'],
                    'user_type': 'customer',
                    'is_verified': True,  # Pre-verified for easy testing
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created customer: {username}')
                )
                
                # Create customer profile
                CustomerProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'emergency_contact': customer_data['phone_number'],
                        'medical_conditions': 'None reported',
                    }
                )
                
            else:
                # Update existing user to be verified
                user.is_verified = True
                user.is_active = True
                user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ Updated existing customer: {username}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Demo customers setup complete!'
                f'\n📊 Created: {created_count} new customers'
                f'\n🔄 Updated: {updated_count} existing customers'
                f'\n\n📋 DEMO CUSTOMER CREDENTIALS:'
                f'\n{"="*50}'
            )
        )
        
        for customer_data in demo_customers:
            self.stdout.write(
                f'\n👤 Username: {customer_data["username"]}'
                f'\n📧 Email: {customer_data["email"]}'
                f'\n🔑 Password: {customer_data["password"]}'
                f'\n👨‍👩‍👧‍👦 Name: {customer_data["first_name"]} {customer_data["last_name"]}'
                f'\n📍 Location: {customer_data["city"]}, {customer_data["country"]}'
                f'\n{"-"*30}'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ All accounts are pre-verified and ready to use!'
                f'\n🚀 You can now login with any of these credentials.'
            )
        )