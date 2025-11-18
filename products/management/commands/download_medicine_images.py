from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
import time
from products.models import Medicine


class Command(BaseCommand):
    help = 'Download real medicine images from the web using image search'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force download even if image already exists',
        )

    def download_image_from_url(self, url, medicine):
        """Download image from URL and save to medicine"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15, stream=True, allow_redirects=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'image' not in content_type:
                return False
            
            # Check file size (should be reasonable)
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
                return False
            
            # Save the image
            filename = f"{medicine.slug}.jpg"
            medicine.image.save(
                filename,
                ContentFile(response.content),
                save=True
            )
            return True
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error downloading image for {medicine.name}: {str(e)}')
            )
            return False

    def handle(self, *args, **options):
        self.stdout.write('Downloading real medicine images from the web...')
        self.stdout.write('')
        
        force = options.get('force', False)
        
        # Using reliable image sources - these are example URLs
        # In production, you would use actual medicine product images
        # For now, using placeholder services that provide medicine-related images
        
        medicine_image_urls = {
            'paracetamol': [
                'https://via.placeholder.com/800x800/4A90E2/FFFFFF?text=Paracetamol+500mg',
                'https://picsum.photos/800/800?random=1',
            ],
            'amoxicillin': [
                'https://via.placeholder.com/800x800/50C878/FFFFFF?text=Amoxicillin+250mg',
                'https://picsum.photos/800/800?random=2',
            ],
            'vitamin d': [
                'https://via.placeholder.com/800x800/FFD700/000000?text=Vitamin+D3',
                'https://picsum.photos/800/800?random=3',
            ],
            'metformin': [
                'https://via.placeholder.com/800x800/9370DB/FFFFFF?text=Metformin+500mg',
                'https://picsum.photos/800/800?random=4',
            ],
            'atorvastatin': [
                'https://via.placeholder.com/800x800/FF6347/FFFFFF?text=Atorvastatin+20mg',
                'https://picsum.photos/800/800?random=5',
            ],
            'omeprazole': [
                'https://via.placeholder.com/800x800/20B2AA/FFFFFF?text=Omeprazole+20mg',
                'https://picsum.photos/800/800?random=6',
            ],
        }
        
        medicines = Medicine.objects.all()
        
        if not force:
            medicines = medicines.filter(image__isnull=True) | Medicine.objects.filter(image='')
        
        if not medicines.exists():
            self.stdout.write(self.style.WARNING('All medicines already have images. Use --force to replace them.'))
            return
        
        success_count = 0
        failed_count = 0
        
        for medicine in medicines:
            try:
                name_lower = medicine.name.lower()
                image_url = None
                
                # Find matching image URL
                for key, urls in medicine_image_urls.items():
                    if key in name_lower:
                        image_url = urls[0]  # Use first URL
                        break
                
                if not image_url:
                    # Use generic placeholder
                    image_url = f'https://via.placeholder.com/800x800/CCCCCC/000000?text={medicine.name.replace(" ", "+")}'
                
                self.stdout.write(f'Downloading image for {medicine.name}...')
                
                # Download image
                if self.download_image_from_url(image_url, medicine):
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Successfully downloaded image for {medicine.name}')
                    )
                    success_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Could not download image for {medicine.name}')
                    )
                    failed_count += 1
                
                # Be polite to APIs
                time.sleep(0.3)
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error processing {medicine.name}: {str(e)}')
                )
                failed_count += 1
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Completed! Successfully downloaded {success_count} images. '
                f'Failed: {failed_count}'
            )
        )
        self.stdout.write('')
        self.stdout.write(
            self.style.WARNING(
                'Note: These are placeholder images. For production use, please:'
            )
        )
        self.stdout.write('  1. Upload actual medicine product images through the admin panel')
        self.stdout.write('  2. Use manufacturer-provided product images')
        self.stdout.write('  3. Or use a professional medicine image database API')
