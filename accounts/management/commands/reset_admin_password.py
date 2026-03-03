from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Reset admin user password'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            help='New password for admin user',
            default='admin123'
        )

    def handle(self, *args, **kwargs):
        password = kwargs['password']
        
        try:
            # Find the admin user
            admin_user = User.objects.get(username='admin')
            
            # Set new password
            admin_user.set_password(password)
            admin_user.save()
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully reset password for admin user: {admin_user.username}'
            ))
            self.stdout.write(self.style.SUCCESS(
                f'New password: {password}'
            ))
            self.stdout.write(self.style.WARNING(
                'Please change this password after logging in!'
            ))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Admin user not found. Creating new admin user...'
            ))
            
            # Create new admin user
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@pharmazone.com.np',
                password=password,
                user_type='admin',
                first_name='Admin',
                last_name='User'
            )
            
            self.stdout.write(self.style.SUCCESS(
                f'Created new admin user: {admin_user.username}'
            ))
            self.stdout.write(self.style.SUCCESS(
                f'Password: {password}'
            ))
