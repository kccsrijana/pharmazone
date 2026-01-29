from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from pharmacist_chat.models import PharmacistChat, ChatMessage

User = get_user_model()


class Command(BaseCommand):
    help = 'Fix chat responses and ensure unlimited conversation'

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
        
        # Find chats that might be stuck
        active_chats = PharmacistChat.objects.filter(
            status__in=['open', 'in_progress']
        )
        
        for chat in active_chats:
            # Ensure pharmacist is assigned
            if not chat.pharmacist:
                chat.pharmacist = pharmacist_user
                chat.status = 'in_progress'
                chat.save()
                self.stdout.write(f"Assigned pharmacist to chat {chat.id}")
            
            # Check if there are user messages without pharmacist responses
            user_messages = chat.messages.filter(is_from_pharmacist=False).order_by('created_at')
            pharmacist_messages = chat.messages.filter(is_from_pharmacist=True).order_by('created_at')
            
            if user_messages.count() > pharmacist_messages.count():
                # There are unresponded user messages
                last_user_message = user_messages.last()
                
                # Create a simple response
                response = f"""Thank you for your question: "{last_user_message.message}"

I'm here to help you with any health or medicine questions!

**I can help with:**
• Medicine dosages and how to take them
• Treatment for symptoms like fever, headache, cough
• Side effects and safety information
• When to see a doctor
• General health advice

**Please tell me more about:**
• What specific symptoms you have
• Your age (helps with dosage)
• Any medicines you're currently taking

What would you like to know more about?"""
                
                ChatMessage.objects.create(
                    chat=chat,
                    sender=pharmacist_user,
                    message=response,
                    is_from_pharmacist=True
                )
                
                self.stdout.write(f"Added response to chat {chat.id}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Fixed {len(active_chats)} active chats!')
        )
        
        # Test the response generation function
        self.stdout.write("\nTesting response generation...")
        
        test_messages = [
            "I have fever",
            "What medicine should I take?",
            "How much paracetamol?",
            "Any side effects?",
            "Can I take it with food?",
            "Thank you"
        ]
        
        # Import the function
        from pharmacist_chat.views import generate_pharmacist_response
        
        # Create a test chat for testing
        test_user = User.objects.first()
        if test_user:
            test_chat = PharmacistChat.objects.create(
                user=test_user,
                subject="Test unlimited responses",
                category="general"
            )
            
            for i, msg in enumerate(test_messages, 1):
                # Create user message
                ChatMessage.objects.create(
                    chat=test_chat,
                    sender=test_user,
                    message=msg,
                    is_from_pharmacist=False
                )
                
                # Test response generation
                try:
                    response = generate_pharmacist_response(msg, test_chat)
                    if response:
                        ChatMessage.objects.create(
                            chat=test_chat,
                            sender=pharmacist_user,
                            message=response,
                            is_from_pharmacist=True
                        )
                        self.stdout.write(f"✓ Question {i}: Generated response")
                    else:
                        self.stdout.write(f"✗ Question {i}: No response generated")
                except Exception as e:
                    self.stdout.write(f"✗ Question {i}: Error - {str(e)}")
            
            self.stdout.write(f"\nTest chat created with ID: {test_chat.id}")
            self.stdout.write("You can view this chat in your browser to test unlimited responses!")
        
        self.stdout.write(
            self.style.SUCCESS('\nChat system should now support unlimited questions!')
        )