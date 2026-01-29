from django.core.management.base import BaseCommand
from pharmacist_chat.models import QuickResponse


class Command(BaseCommand):
    help = 'Add sample quick responses for pharmacist chat'

    def handle(self, *args, **options):
        quick_responses = [
            # General Questions
            {
                'category': 'general',
                'question': 'What are the pharmacy operating hours?',
                'answer': 'Our pharmacy is open Monday to Saturday from 8:00 AM to 8:00 PM, and Sunday from 10:00 AM to 6:00 PM. We also offer 24/7 online ordering and consultation services.'
            },
            {
                'category': 'general',
                'question': 'Do you deliver medicines to my location?',
                'answer': 'Yes, we deliver medicines throughout Nepal. Delivery is free for orders above Rs. 2000. For orders below Rs. 2000, a delivery charge of Rs. 100 applies. Delivery usually takes 1-3 business days depending on your location.'
            },
            {
                'category': 'general',
                'question': 'Can I return medicines if I don\'t need them?',
                'answer': 'Due to safety regulations, we cannot accept returns of medicines once they have been dispensed. However, if there was an error in your order or the medicine is damaged, please contact us within 24 hours for a replacement.'
            },
            
            # Dosage Information
            {
                'category': 'dosage',
                'question': 'How should I take Paracetamol for fever?',
                'answer': 'For adults: Take 500-1000mg (1-2 tablets) every 4-6 hours as needed. Do not exceed 4000mg (8 tablets) in 24 hours. For children, dosage depends on weight - consult your doctor. Take with or after food to reduce stomach irritation.'
            },
            {
                'category': 'dosage',
                'question': 'What if I miss a dose of my medication?',
                'answer': 'If you miss a dose, take it as soon as you remember. However, if it\'s almost time for your next dose, skip the missed dose and continue with your regular schedule. Never take a double dose to make up for a missed one. For critical medications, consult your doctor.'
            },
            {
                'category': 'dosage',
                'question': 'Can I take medicine with milk or juice?',
                'answer': 'Most medicines should be taken with water. Milk can interfere with some antibiotics, and acidic juices can affect certain medications. Always read the label or ask your pharmacist. When in doubt, stick to plain water.'
            },
            
            # Side Effects
            {
                'category': 'side_effects',
                'question': 'What are common side effects of antibiotics?',
                'answer': 'Common antibiotic side effects include: nausea, diarrhea, stomach upset, yeast infections, and allergic reactions. Take with food to reduce stomach issues. Complete the full course even if you feel better. Contact your doctor if you experience severe reactions.'
            },
            {
                'category': 'side_effects',
                'question': 'When should I stop taking a medicine due to side effects?',
                'answer': 'Stop immediately and seek medical help if you experience: severe allergic reactions (rash, swelling, difficulty breathing), severe nausea/vomiting, unusual bleeding, or any symptoms that concern you. For mild side effects, consult your doctor before stopping.'
            },
            
            # Drug Interactions
            {
                'category': 'interactions',
                'question': 'Can I take multiple medicines together?',
                'answer': 'Some medicines can interact with each other, affecting their effectiveness or causing side effects. Always inform your doctor and pharmacist about all medicines you\'re taking, including over-the-counter drugs and supplements. We can check for interactions.'
            },
            {
                'category': 'interactions',
                'question': 'Is it safe to drink alcohol while taking medication?',
                'answer': 'Alcohol can interact with many medications, increasing side effects or reducing effectiveness. It\'s especially dangerous with antibiotics, pain relievers, and blood thinners. Always check with your pharmacist or read the medication label for alcohol warnings.'
            },
            
            # Prescription Help
            {
                'category': 'prescription',
                'question': 'My prescription is expired, can I still get the medicine?',
                'answer': 'Expired prescriptions cannot be filled for safety reasons. You\'ll need a new prescription from your doctor. For chronic conditions, ask your doctor for refills or a longer-term prescription to avoid interruptions in your treatment.'
            },
            {
                'category': 'prescription',
                'question': 'Can I get a generic version of my prescribed medicine?',
                'answer': 'Yes, generic medicines contain the same active ingredients as brand-name drugs and are equally effective. They\'re usually much cheaper. We can substitute with generics unless your doctor specifically writes "brand necessary" on the prescription.'
            },
            
            # Symptom-based Recommendations
            {
                'category': 'symptoms',
                'question': 'What can I take for a headache?',
                'answer': 'For mild to moderate headaches, you can try: Paracetamol (500-1000mg), Ibuprofen (400mg), or Aspirin (500mg). Drink plenty of water, rest in a quiet dark room. If headaches are frequent or severe, consult a doctor.'
            },
            {
                'category': 'symptoms',
                'question': 'What medicine is good for cold and cough?',
                'answer': 'For cold symptoms: Paracetamol for fever/aches, saline nasal drops for congestion. For dry cough: dextromethorphan-based syrups. For productive cough: expectorants like bromhexine. Drink warm fluids and rest. See a doctor if symptoms persist beyond 7 days.'
            },
            {
                'category': 'symptoms',
                'question': 'What can I take for stomach upset?',
                'answer': 'For mild stomach upset: ORS for hydration, probiotics for gut health. For acidity: antacids like ENO or Gelusil. For nausea: ginger tea or domperidone. Eat bland foods (rice, banana). Consult a doctor if symptoms are severe or persist.'
            },
        ]

        for response_data in quick_responses:
            response, created = QuickResponse.objects.get_or_create(
                category=response_data['category'],
                question=response_data['question'],
                defaults={
                    'answer': response_data['answer'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f"Created quick response: {response_data['question']}")
            else:
                self.stdout.write(f"Quick response already exists: {response_data['question']}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(quick_responses)} quick responses!'
            )
        )