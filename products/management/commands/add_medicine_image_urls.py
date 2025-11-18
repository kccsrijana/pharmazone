from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from products.models import Medicine


class Command(BaseCommand):
    help = 'Add medicine images by downloading from provided URLs or using image search'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Direct image URL to download',
        )
        parser.add_argument(
            '--medicine-id',
            type=int,
            help='Medicine ID to update',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Update all medicines with sample image URLs',
        )

    def download_image(self, url, medicine):
        """Download image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15, stream=True, allow_redirects=True)
            response.raise_for_status()
            
            # Verify it's an image
            content_type = response.headers.get('content-type', '').lower()
            if 'image' not in content_type:
                return False, "URL does not point to an image"
            
            # Save image
            filename = f"{medicine.slug}.jpg"
            medicine.image.save(filename, ContentFile(response.content), save=True)
            return True, "Image downloaded successfully"
            
        except Exception as e:
            return False, str(e)

    def handle(self, *args, **options):
        if options['url'] and options['medicine_id']:
            # Download specific image for specific medicine
            try:
                medicine = Medicine.objects.get(id=options['medicine_id'])
                success, message = self.download_image(options['url'], medicine)
                if success:
                    self.stdout.write(self.style.SUCCESS(f'✓ {message} for {medicine.name}'))
                else:
                    self.stdout.write(self.style.ERROR(f'✗ Failed: {message}'))
            except Medicine.DoesNotExist:
                self.stdout.write(self.style.ERROR('Medicine not found'))
        
        elif options['all']:
            # Use image search URLs - these would need to be actual medicine image URLs
            # For now, providing a template that users can modify
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('To add real medicine images:'))
            self.stdout.write('')
            self.stdout.write('Option 1: Use the admin panel')
            self.stdout.write('  1. Go to http://127.0.0.1:8000/admin/')
            self.stdout.write('  2. Navigate to Products > Medicines')
            self.stdout.write('  3. Click on a medicine')
            self.stdout.write('  4. Upload an image file or paste an image URL')
            self.stdout.write('')
            self.stdout.write('Option 2: Use this command with image URLs')
            self.stdout.write('  python manage.py add_medicine_image_urls --url "IMAGE_URL" --medicine-id MEDICINE_ID')
            self.stdout.write('')
            self.stdout.write('Option 3: Find medicine images from:')
            self.stdout.write('  - Manufacturer websites')
            self.stdout.write('  - Pharmacy websites')
            self.stdout.write('  - Medicine databases')
            self.stdout.write('  - Stock photo sites (with proper licensing)')
            self.stdout.write('')
            
            # Provide example image URLs that users can replace
            medicines = Medicine.objects.all()
            self.stdout.write('Example usage:')
            for medicine in medicines:
                self.stdout.write(f'  python manage.py add_medicine_image_urls --url "YOUR_IMAGE_URL_HERE" --medicine-id {medicine.id}')
        
        else:
            self.stdout.write(self.style.ERROR('Please provide either --url and --medicine-id, or --all'))
            self.stdout.write('')
            self.stdout.write('Usage examples:')
            self.stdout.write('  python manage.py add_medicine_image_urls --url "https://example.com/image.jpg" --medicine-id 1')
            self.stdout.write('  python manage.py add_medicine_image_urls --all')


