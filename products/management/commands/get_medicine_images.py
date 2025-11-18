from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
import time
from products.models import Medicine


class Command(BaseCommand):
    help = 'Download real medicine images from the web'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Image URL to download',
        )
        parser.add_argument(
            '--id',
            type=int,
            help='Medicine ID',
        )

    def download_image(self, image_url, medicine):
        """Download and save image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            response = requests.get(image_url, headers=headers, timeout=20, stream=True, allow_redirects=True)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('content-type', '').lower()
            if 'image' not in content_type:
                return False, f"URL returned {content_type}, not an image"
            
            # Check file size (max 5MB)
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > 5 * 1024 * 1024:
                return False, "Image file too large (>5MB)"
            
            # Determine file extension from content type or URL
            ext = 'jpg'
            if 'png' in content_type:
                ext = 'png'
            elif 'gif' in content_type:
                ext = 'gif'
            elif 'webp' in content_type:
                ext = 'webp'
            
            # Save the image
            filename = f"{medicine.slug}.{ext}"
            medicine.image.save(filename, ContentFile(response.content), save=True)
            return True, f"Image saved as {filename}"
            
        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('Medicine Image Downloader'))
        self.stdout.write('=' * 60)
        self.stdout.write('')
        
        medicines = Medicine.objects.all()
        
        self.stdout.write(self.style.WARNING('To add real medicine images, you have two options:'))
        self.stdout.write('')
        self.stdout.write('OPTION 1: Manual Image URLs (Recommended)')
        self.stdout.write('  Find medicine images from:')
        self.stdout.write('    - Google Images (images.google.com)')
        self.stdout.write('    - Manufacturer websites')
        self.stdout.write('    - Pharmacy websites')
        self.stdout.write('    - Medicine databases')
        self.stdout.write('')
        self.stdout.write('  Then run:')
        self.stdout.write('    python manage.py get_medicine_images --url "IMAGE_URL" --id MEDICINE_ID')
        self.stdout.write('')
        self.stdout.write('OPTION 2: Admin Panel (Easiest)')
        self.stdout.write('  1. Go to http://127.0.0.1:8000/admin/')
        self.stdout.write('  2. Products > Medicines')
        self.stdout.write('  3. Click on a medicine')
        self.stdout.write('  4. Upload image file or paste image URL')
        self.stdout.write('')
        self.stdout.write('=' * 60)
        self.stdout.write('')
        self.stdout.write('Current medicines:')
        self.stdout.write('')
        
        for medicine in medicines:
            has_image = "✓ Has image" if medicine.image else "✗ No image"
            self.stdout.write(f'  ID {medicine.id}: {medicine.name} - {has_image}')
        
        self.stdout.write('')
        self.stdout.write('Example command:')
        self.stdout.write('  python manage.py get_medicine_images --url "https://example.com/paracetamol.jpg" --id 1')
        self.stdout.write('')
        
        # If URL and ID provided, download the image
        if options.get('url') and options.get('id'):
            try:
                medicine = Medicine.objects.get(id=options['id'])
                self.stdout.write(f'Downloading image for {medicine.name}...')
                success, message = self.download_image(options['url'], medicine)
                
                if success:
                    self.stdout.write(self.style.SUCCESS(f'✓ {message}'))
                    self.stdout.write(self.style.SUCCESS(f'Image successfully added to {medicine.name}!'))
                else:
                    self.stdout.write(self.style.ERROR(f'✗ Failed: {message}'))
                    self.stdout.write(self.style.WARNING('Please check the URL and try again.'))
            except Medicine.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Medicine with ID {options["id"]} not found'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

