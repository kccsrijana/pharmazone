from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Remove or convert pharmacy user type to customer'

    def handle(self, *args, **kwargs):
        # Find all pharmacy users
        pharmacy_users = User.objects.filter(user_type='pharmacy')
        count = pharmacy_users.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No pharmacy users found.'))
            return
        
        self.stdout.write(f'Found {count} pharmacy user(s).')
        
        # Convert pharmacy users to customer type
        pharmacy_users.update(user_type='customer')
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully converted {count} pharmacy user(s) to customer type.'
        ))
