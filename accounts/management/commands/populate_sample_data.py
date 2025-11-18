from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Manufacturer, Medicine
from accounts.models import PharmacyProfile, CustomerProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Pain Relief', 'description': 'Medicines for pain management and relief'},
            {'name': 'Antibiotics', 'description': 'Antibacterial medications'},
            {'name': 'Vitamins', 'description': 'Vitamin supplements and multivitamins'},
            {'name': 'Diabetes', 'description': 'Medicines for diabetes management'},
            {'name': 'Heart Health', 'description': 'Cardiovascular medications'},
            {'name': 'Digestive Health', 'description': 'Medicines for digestive issues'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create manufacturers
        manufacturers_data = [
            {'name': 'Sun Pharma', 'country': 'India'},
            {'name': 'Cipla', 'country': 'India'},
            {'name': 'Dr. Reddy\'s', 'country': 'India'},
            {'name': 'Lupin', 'country': 'India'},
            {'name': 'Aurobindo Pharma', 'country': 'India'},
        ]
        
        manufacturers = []
        for man_data in manufacturers_data:
            manufacturer, created = Manufacturer.objects.get_or_create(
                name=man_data['name'],
                defaults={'country': man_data['country']}
            )
            manufacturers.append(manufacturer)
            if created:
                self.stdout.write(f'Created manufacturer: {manufacturer.name}')
        
        # Create sample medicines
        medicines_data = [
            {
                'name': 'Paracetamol 500mg',
                'generic_name': 'Acetaminophen',
                'category': 'Pain Relief',
                'manufacturer': 'Sun Pharma',
                'prescription_type': 'otc',
                'dosage_form': 'Tablet',
                'strength': '500mg',
                'pack_size': '10 tablets',
                'price': 25.00,
                'stock_quantity': 100,
                'description': 'Effective pain relief and fever reducer',
                'indications': 'Headache, fever, body pain',
            },
            {
                'name': 'Amoxicillin 250mg',
                'generic_name': 'Amoxicillin',
                'category': 'Antibiotics',
                'manufacturer': 'Cipla',
                'prescription_type': 'prescription',
                'dosage_form': 'Capsule',
                'strength': '250mg',
                'pack_size': '10 capsules',
                'price': 45.00,
                'stock_quantity': 50,
                'description': 'Broad spectrum antibiotic',
                'indications': 'Bacterial infections',
            },
            {
                'name': 'Vitamin D3',
                'generic_name': 'Cholecalciferol',
                'category': 'Vitamins',
                'manufacturer': 'Dr. Reddy\'s',
                'prescription_type': 'otc',
                'dosage_form': 'Tablet',
                'strength': '60,000 IU',
                'pack_size': '4 tablets',
                'price': 120.00,
                'stock_quantity': 75,
                'description': 'Vitamin D supplement for bone health',
                'indications': 'Vitamin D deficiency',
            },
            {
                'name': 'Metformin 500mg',
                'generic_name': 'Metformin',
                'category': 'Diabetes',
                'manufacturer': 'Lupin',
                'prescription_type': 'prescription',
                'dosage_form': 'Tablet',
                'strength': '500mg',
                'pack_size': '10 tablets',
                'price': 35.00,
                'stock_quantity': 60,
                'description': 'Antidiabetic medication',
                'indications': 'Type 2 diabetes',
            },
            {
                'name': 'Atorvastatin 20mg',
                'generic_name': 'Atorvastatin',
                'category': 'Heart Health',
                'manufacturer': 'Aurobindo Pharma',
                'prescription_type': 'prescription',
                'dosage_form': 'Tablet',
                'strength': '20mg',
                'pack_size': '10 tablets',
                'price': 55.00,
                'stock_quantity': 40,
                'description': 'Cholesterol lowering medication',
                'indications': 'High cholesterol',
            },
            {
                'name': 'Omeprazole 20mg',
                'generic_name': 'Omeprazole',
                'category': 'Digestive Health',
                'manufacturer': 'Sun Pharma',
                'prescription_type': 'otc',
                'dosage_form': 'Capsule',
                'strength': '20mg',
                'pack_size': '10 capsules',
                'price': 65.00,
                'stock_quantity': 80,
                'description': 'Proton pump inhibitor for acid reflux',
                'indications': 'Acid reflux, heartburn',
            },
        ]
        
        for med_data in medicines_data:
            category = next(cat for cat in categories if cat.name == med_data['category'])
            manufacturer = next(man for man in manufacturers if man.name == med_data['manufacturer'])
            
            medicine, created = Medicine.objects.get_or_create(
                name=med_data['name'],
                defaults={
                    'generic_name': med_data['generic_name'],
                    'category': category,
                    'manufacturer': manufacturer,
                    'prescription_type': med_data['prescription_type'],
                    'dosage_form': med_data['dosage_form'],
                    'strength': med_data['strength'],
                    'pack_size': med_data['pack_size'],
                    'price': med_data['price'],
                    'stock_quantity': med_data['stock_quantity'],
                    'description': med_data['description'],
                    'indications': med_data['indications'],
                    'is_featured': True,
                }
            )
            if created:
                self.stdout.write(f'Created medicine: {medicine.name}')
        
        # Create sample users
        # Customer user
        customer_user, created = User.objects.get_or_create(
            username='customer1',
            defaults={
                'email': 'customer1@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '+9779876543210',
                'user_type': 'customer',
                'is_verified': True,
            }
        )
        if created:
            customer_user.set_password('customer123')
            customer_user.save()
            CustomerProfile.objects.create(user=customer_user)
            self.stdout.write('Created customer user: customer1')
        
        # Pharmacy user
        pharmacy_user, created = User.objects.get_or_create(
            username='pharmacy1',
            defaults={
                'email': 'pharmacy1@example.com',
                'first_name': 'Medi',
                'last_name': 'Care',
                'phone_number': '+9779876543211',
                'user_type': 'pharmacy',
                'is_verified': True,
            }
        )
        if created:
            pharmacy_user.set_password('pharmacy123')
            pharmacy_user.save()
            PharmacyProfile.objects.create(
                user=pharmacy_user,
                pharmacy_name='MediCare Pharmacy',
                license_number='PH123456',
                gst_number='29ABCDE1234F1Z5',
                description='Your trusted neighborhood pharmacy',
                is_approved=True,
            )
            self.stdout.write('Created pharmacy user: pharmacy1')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write('\nSample users created:')
        self.stdout.write('Customer: username=customer1, password=customer123')
        self.stdout.write('Pharmacy: username=pharmacy1, password=pharmacy123')
        self.stdout.write('Admin: username=admin, password=admin123')
