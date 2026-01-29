from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import User

class Command(BaseCommand):
    help = 'Create an admin user for testing appointment management'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if admin user already exists
        if User.objects.filter(username='admin', user_type='admin').exists():
            self.stdout.write(
                self.style.WARNING('Admin user already exists!')
            )
            return
        
        # Create admin user
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@pharmazone.com.np',
            password='admin123',
            first_name='Admin',
            last_name='User',
            user_type='admin',
            is_staff=True,
            is_superuser=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created admin user: {admin_user.username}\n'
                f'Email: {admin_user.email}\n'
                f'Password: admin123\n'
                f'User Type: {admin_user.user_type}'
            )
        )