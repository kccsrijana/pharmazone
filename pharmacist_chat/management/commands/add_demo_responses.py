from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from pharmacist_chat.models import PharmacistChat, ChatMessage

User = get_user_model()


class Command(BaseCommand):
    help = 'Add demo pharmacist responses to existing chats'

    def handle(self, *args, **options):
        # Get or create demo pharmacist
        pharmacist_user, created = User.objects.get_or_create(
            username='pharmacist_demo',
            defaults={
                'first_name': 'Demo',
                'last_name': 'Pharmacist',
                'email': 'pharmacist@pharmazone.com',
                'is_staff': True
            }
        )
        
        if created:
            pharmacist_user.set_password('demo123')
            pharmacist_user.save()
            self.stdout.write("Created demo pharmacist user")
        
        # Find chats without pharmacist responses
        open_chats = PharmacistChat.objects.filter(
            status='open',
            pharmacist__isnull=True
        )
        
        for chat in open_chats:
            # Assign pharmacist
            chat.pharmacist = pharmacist_user
            chat.status = 'in_progress'
            chat.save()
            
            # Create response based on subject
            subject_lower = chat.subject.lower()
            
            if 'fever' in subject_lower:
                response = """Hello! I'm here to help you with fever symptoms.

**Common fever symptoms include:**
• Body temperature above 100.4°F (38°C)
• Chills and shivering
• Headache
• Muscle aches and weakness
• Loss of appetite
• Dehydration
• General discomfort

**For fever management:**
• Take Paracetamol 500-1000mg every 4-6 hours (max 4000mg/day)
• Drink plenty of fluids
• Rest and avoid strenuous activities
• Use cool compresses on forehead

**When to see a doctor:**
• Fever above 103°F (39.4°C)
• Fever lasting more than 3 days
• Severe headache or neck stiffness
• Difficulty breathing
• Persistent vomiting

Do you have any specific questions about your fever or need medicine recommendations?"""
            else:
                response = f"""Hello! Thank you for your question about "{chat.subject}".

I'm here to help with any questions about:
• Medicine dosages and usage
• Side effects and interactions
• Symptom-based recommendations
• General health advice

Please provide more details about your specific situation, and I'll be happy to give you personalized advice. What additional information can you share?"""
            
            # Create pharmacist message
            ChatMessage.objects.create(
                chat=chat,
                sender=pharmacist_user,
                message=response,
                is_from_pharmacist=True
            )
            
            self.stdout.write(f"Added response to chat: {chat.subject}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Added responses to {len(open_chats)} chats!')
        )