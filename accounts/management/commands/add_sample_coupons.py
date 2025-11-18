from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from payments.models import Coupon
from products.models import Category


class Command(BaseCommand):
    help = 'Add sample coupons to the database'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample coupons...')
        
        # Get some categories for coupon restrictions
        categories = Category.objects.all()
        
        # Create sample coupons
        coupons_data = [
            {
                'code': 'WELCOME10',
                'description': 'Welcome discount for new customers',
                'coupon_type': 'percentage',
                'value': 10,
                'minimum_order_amount': 1000,
                'usage_limit': 100,
                'usage_limit_per_user': 1,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=30),
                'is_active': True,
            },
            {
                'code': 'SAVE50',
                'description': 'Flat Rs. 50 off on orders above Rs. 5000',
                'coupon_type': 'fixed',
                'value': 50,
                'minimum_order_amount': 5000,
                'usage_limit': 50,
                'usage_limit_per_user': 2,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=15),
                'is_active': True,
            },
            {
                'code': 'MEDICINE20',
                'description': '20% off on all medicines',
                'coupon_type': 'percentage',
                'value': 20,
                'minimum_order_amount': 2000,
                'maximum_discount': 200,
                'usage_limit': 200,
                'usage_limit_per_user': 3,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=45),
                'is_active': True,
            },
            {
                'code': 'FIRSTORDER',
                'description': 'Special discount for first order',
                'coupon_type': 'percentage',
                'value': 15,
                'minimum_order_amount': 3000,
                'usage_limit': 1000,
                'usage_limit_per_user': 1,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=60),
                'is_active': True,
            },
        ]
        
        for coupon_data in coupons_data:
            coupon, created = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
            if created:
                self.stdout.write(f'Created coupon: {coupon.code}')
            else:
                self.stdout.write(f'Coupon {coupon.code} already exists')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample coupons!')
        )
        self.stdout.write('\nSample coupons created:')
        self.stdout.write('WELCOME10 - 10% off (min Rs. 1000)')
        self.stdout.write('SAVE50 - Rs. 50 off (min Rs. 5000)')
        self.stdout.write('MEDICINE20 - 20% off medicines (min Rs. 2000)')
        self.stdout.write('FIRSTORDER - 15% off first order (min Rs. 3000)')
