from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from pharmacist_chat.models import PharmacistChat, ChatMessage
from pharmacist_chat.views import generate_pharmacist_response

User = get_user_model()


class Command(BaseCommand):
    help = 'Test the chatbot responses'

    def handle(self, *args, **options):
        # Test various user messages
        test_messages = [
            "Hello, I have a headache",
            "What dosage of paracetamol should I take?",
            "I'm 25 years old and weigh 70kg",
            "Are there any side effects?",
            "Can I take it with ibuprofen?",
            "Thank you for your help"
        ]
        
        # Create a test chat
        test_user = User.objects.first()
        if not test_user:
            self.stdout.write("No users found. Please create a user first.")
            return
        
        chat = PharmacistChat.objects.create(
            user=test_user,
            subject="Test chatbot conversation",
            category="general"
        )
        
        self.stdout.write(f"Created test chat: {chat.id}")
        
        for i, message_text in enumerate(test_messages, 1):
            # Create user message
            user_message = ChatMessage.objects.create(
                chat=chat,
                sender=test_user,
                message=message_text,
                is_from_pharmacist=False
            )
            
            self.stdout.write(f"\n{i}. USER: {message_text}")
            
            # Generate bot response
            response = generate_pharmacist_response(message_text, chat)
            
            if response:
                # Create bot response
                pharmacist_user, _ = User.objects.get_or_create(
                    username='pharmacist_demo',
                    defaults={
                        'first_name': 'Demo',
                        'last_name': 'Pharmacist',
                        'email': 'pharmacist@pharmazone.com',
                        'is_staff': True
                    }
                )
                
                ChatMessage.objects.create(
                    chat=chat,
                    sender=pharmacist_user,
                    message=response,
                    is_from_pharmacist=True
                )
                
                self.stdout.write(f"   PHARMACIST: {response[:100]}...")
            else:
                self.stdout.write("   PHARMACIST: No response generated")
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTest completed! Check chat ID {chat.id} in your browser.')
        )