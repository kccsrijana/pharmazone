from django.core.management.base import BaseCommand
from products.models import Medicine, Category, Manufacturer
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Add two new featured medicines'

    def handle(self, *args, **kwargs):
        # Get categories and manufacturers
        antibiotics = Category.objects.get(name='Antibiotics')
        vitamins = Category.objects.get(name='Vitamins')
        cipla = Manufacturer.objects.get(name='Cipla')
        sun_pharma = Manufacturer.objects.get(name='Sun Pharma')
        
        # Medicine 1: Azithromycin (Antibiotic)
        medicine1, created1 = Medicine.objects.get_or_create(
            name='Azithromycin',
            strength='500mg',
            defaults={
                'generic_name': 'Azithromycin',
                'description': 'Azithromycin is a macrolide antibiotic used to treat various bacterial infections including respiratory infections, skin infections, ear infections, and sexually transmitted diseases.',
                'category': antibiotics,
                'manufacturer': cipla,
                'prescription_type': 'prescription',
                'dosage_form': 'Tablet',
                'pack_size': '3 tablets',
                'composition': 'Azithromycin 500mg',
                'indications': 'Respiratory tract infections, skin and soft tissue infections, ear infections, sexually transmitted infections',
                'contraindications': 'Hypersensitivity to azithromycin or other macrolide antibiotics, severe liver disease',
                'side_effects': 'Nausea, diarrhea, abdominal pain, headache, dizziness',
                'storage_conditions': 'Store at room temperature (15-30°C), away from moisture and direct sunlight',
                'expiry_date': date.today() + timedelta(days=730),  # 2 years from now
                'price': 150.00,
                'stock_quantity': 200,
                'min_order_quantity': 1,
                'max_order_quantity': 10,
                'is_active': True,
                'is_featured': True,
                'requires_prescription': True,
            }
        )
        
        if created1:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {medicine1.name} {medicine1.strength}'))
        else:
            medicine1.is_featured = True
            medicine1.save()
            self.stdout.write(self.style.WARNING(f'⚠ Already exists (marked as featured): {medicine1.name} {medicine1.strength}'))
        
        # Medicine 2: Vitamin B Complex
        medicine2, created2 = Medicine.objects.get_or_create(
            name='Vitamin B Complex',
            strength='High Potency',
            defaults={
                'generic_name': 'B-Complex Vitamins',
                'description': 'A comprehensive B-complex supplement containing all 8 essential B vitamins to support energy production, nervous system health, and overall wellness.',
                'category': vitamins,
                'manufacturer': sun_pharma,
                'prescription_type': 'otc',
                'dosage_form': 'Capsule',
                'pack_size': '30 capsules',
                'composition': 'Thiamine (B1) 10mg, Riboflavin (B2) 10mg, Niacin (B3) 50mg, Pantothenic Acid (B5) 25mg, Pyridoxine (B6) 10mg, Biotin (B7) 300mcg, Folic Acid (B9) 400mcg, Cobalamin (B12) 50mcg',
                'indications': 'Energy support, nervous system health, metabolism support, stress management, healthy skin and hair',
                'contraindications': 'Hypersensitivity to any B vitamins',
                'side_effects': 'Generally well tolerated. May cause mild nausea or stomach upset in some individuals',
                'storage_conditions': 'Store in a cool, dry place away from direct sunlight',
                'expiry_date': date.today() + timedelta(days=730),  # 2 years from now
                'price': 299.00,
                'stock_quantity': 150,
                'min_order_quantity': 1,
                'max_order_quantity': 20,
                'is_active': True,
                'is_featured': True,
                'requires_prescription': False,
            }
        )
        
        if created2:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {medicine2.name} {medicine2.strength}'))
        else:
            medicine2.is_featured = True
            medicine2.save()
            self.stdout.write(self.style.WARNING(f'⚠ Already exists (marked as featured): {medicine2.name} {medicine2.strength}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Successfully added 2 new featured medicines!'))
        self.stdout.write(self.style.SUCCESS(f'Total featured medicines: {Medicine.objects.filter(is_featured=True).count()}'))
