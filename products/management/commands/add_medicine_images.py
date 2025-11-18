from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
import io
from products.models import Medicine


class Command(BaseCommand):
    help = 'Add placeholder images to medicines that don\'t have images'

    def handle(self, *args, **options):
        self.stdout.write('Adding images to medicines...')
        
        medicines = Medicine.objects.filter(image__isnull=True) | Medicine.objects.filter(image='')
        
        if not medicines.exists():
            self.stdout.write(self.style.WARNING('All medicines already have images.'))
            return
        
        for medicine in medicines:
            try:
                # Create a placeholder image
                img = Image.new('RGB', (400, 400), color='#f0f0f0')
                draw = ImageDraw.Draw(img)
                
                # Add a border
                draw.rectangle([10, 10, 390, 390], outline='#007bff', width=3)
                
                # Add medicine icon (pill shape)
                # Draw a pill shape
                pill_coords = [(100, 150), (300, 250)]
                draw.ellipse([100, 150, 200, 200], fill='#007bff', outline='#0056b3', width=2)
                draw.ellipse([200, 150, 300, 200], fill='#007bff', outline='#0056b3', width=2)
                draw.rectangle([150, 150, 250, 200], fill='#007bff')
                
                # Add text (medicine name, truncated if too long)
                try:
                    # Try to use a default font
                    font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
                    font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
                except:
                    # Fallback to default font
                    font_large = ImageFont.load_default()
                    font_small = ImageFont.load_default()
                
                # Add medicine name
                name = medicine.name[:20] if len(medicine.name) > 20 else medicine.name
                bbox = draw.textbbox((0, 0), name, font=font_large)
                text_width = bbox[2] - bbox[0]
                text_x = (400 - text_width) // 2
                draw.text((text_x, 260), name, fill='#333333', font=font_large)
                
                # Add strength if available
                if medicine.strength:
                    strength = medicine.strength[:15] if len(medicine.strength) > 15 else medicine.strength
                    bbox = draw.textbbox((0, 0), strength, font=font_small)
                    text_width = bbox[2] - bbox[0]
                    text_x = (400 - text_width) // 2
                    draw.text((text_x, 300), strength, fill='#666666', font=font_small)
                
                # Add "Pharmazone" text at bottom
                bbox = draw.textbbox((0, 0), "Pharmazone", font=font_small)
                text_width = bbox[2] - bbox[0]
                text_x = (400 - text_width) // 2
                draw.text((text_x, 350), "Pharmazone", fill='#007bff', font=font_small)
                
                # Save to BytesIO
                img_io = io.BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                
                # Save to medicine
                filename = f"{medicine.slug}.png"
                medicine.image.save(filename, ContentFile(img_io.read()), save=True)
                
                self.stdout.write(f'✓ Added image to {medicine.name}')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error adding image to {medicine.name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added images to {medicines.count()} medicines!')
        )

