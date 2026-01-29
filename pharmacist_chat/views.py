from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import PharmacistChat, ChatMessage, PharmacistProfile, QuickResponse
from .forms import StartChatForm, ChatMessageForm


def ask_pharmacist_home(request):
    """Ask a Pharmacist home page with quick responses"""
    try:
        quick_responses = QuickResponse.objects.filter(is_active=True).order_by('category', 'question')
        
        # Group quick responses by category
        grouped_responses = {}
        for response in quick_responses:
            category = response.get_category_display()
            if category not in grouped_responses:
                grouped_responses[category] = []
            grouped_responses[category].append(response)
        
        context = {
            'grouped_responses': grouped_responses,
            'categories': PharmacistChat.CATEGORY_CHOICES,
        }
        return render(request, 'pharmacist_chat/home.html', context)
    except Exception as e:
        # Fallback if there's an error
        context = {
            'grouped_responses': {},
            'categories': PharmacistChat.CATEGORY_CHOICES,
            'error': str(e)
        }
        return render(request, 'pharmacist_chat/home.html', context)


@login_required
def start_chat(request):
    """Start a new chat with pharmacist"""
    if request.method == 'POST':
        form = StartChatForm(request.POST)
        if form.is_valid():
            try:
                chat = form.save(commit=False)
                chat.user = request.user
                chat.save()
                
                # Create initial message
                initial_message = f"Hi! I need help with: {chat.subject}"
                ChatMessage.objects.create(
                    chat=chat,
                    sender=request.user,
                    message=initial_message,
                    is_from_pharmacist=False
                )
                
                # Auto-response from pharmacist (for demo purposes)
                import time
                time.sleep(1)  # Small delay to simulate thinking
                
                # Create a demo pharmacist response
                auto_response = get_auto_response(chat.category, chat.subject)
                if auto_response:
                    # Get or create a pharmacist user
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    pharmacist_user, created = User.objects.get_or_create(
                        username='pharmacist_demo',
                        defaults={
                            'first_name': 'Demo',
                            'last_name': 'Pharmacist',
                            'email': 'pharmacist@pharmazone.com',
                            'is_staff': True
                        }
                    )
                    
                    # Assign pharmacist to chat
                    chat.pharmacist = pharmacist_user
                    chat.status = 'in_progress'
                    chat.save()
                    
                    # Create pharmacist response
                    ChatMessage.objects.create(
                        chat=chat,
                        sender=pharmacist_user,
                        message=auto_response,
                        is_from_pharmacist=True
                    )
                
                messages.success(request, 'Your chat has been started! A pharmacist will respond shortly.')
                return redirect('pharmacist_chat:chat_detail', chat_id=chat.id)
            except Exception as e:
                messages.error(request, f'Error starting chat: {str(e)}')
                return redirect('pharmacist_chat:start_chat')
        else:
            # Form has validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StartChatForm()
    
    context = {
        'form': form,
    }
    return render(request, 'pharmacist_chat/start_chat.html', context)


def get_auto_response(category, subject):
    """Generate automatic response based on category and subject"""
    subject_lower = subject.lower()
    
    # Fever-related responses
    if 'fever' in subject_lower:
        return """Hello! I'm here to help you with fever symptoms.

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
    
    # Headache responses
    elif 'headache' in subject_lower:
        return """I can help you with headache relief.

**For headache treatment:**
• Paracetamol 500-1000mg every 4-6 hours
• Ibuprofen 400mg every 6-8 hours
• Rest in a quiet, dark room
• Apply cold or warm compress
• Stay hydrated

**When to consult a doctor:**
• Sudden severe headache
• Headache with fever and neck stiffness
• Frequent headaches
• Headache after head injury

What type of headache are you experiencing? Is it mild, moderate, or severe?"""
    
    # Cough responses
    elif 'cough' in subject_lower:
        return """I can help you with cough treatment.

**For dry cough:**
• Dextromethorphan-based cough syrups
• Honey and warm water
• Steam inhalation

**For productive cough:**
• Bromhexine or Ambroxol syrups
• Plenty of warm fluids
• Avoid cough suppressants

**General advice:**
• Stay hydrated
• Use a humidifier
• Avoid irritants like smoke

How long have you had this cough? Is it dry or producing phlegm?"""
    
    # General responses by category
    elif category == 'dosage':
        return """Hello! I'm here to help with dosage information.

Please provide me with:
• The name of the medicine
• Your age and weight (if comfortable sharing)
• Any other medications you're taking
• The condition you're treating

This will help me give you accurate dosage guidance. What specific medicine do you need help with?"""
    
    elif category == 'side_effects':
        return """I can help you understand side effects.

Please tell me:
• Which medicine are you concerned about?
• What symptoms are you experiencing?
• How long have you been taking the medicine?
• Any other medications you're on?

This information will help me assess if what you're experiencing is related to the medication."""
    
    elif category == 'interactions':
        return """I can help check for drug interactions.

Please provide:
• List of all medicines you're currently taking
• Any new medicine you want to add
• Any supplements or herbal products
• Your medical conditions

Drug interactions can be serious, so it's important to check before combining medications."""
    
    else:
        return """Hello! Thank you for contacting our pharmacy.

I'm here to help with any questions about:
• Medicine dosages and usage
• Side effects and interactions
• Symptom-based recommendations
• General health advice

Please provide more details about your question, and I'll be happy to assist you. What specific help do you need today?"""


@login_required
def chat_detail(request, chat_id):
    """View and participate in a chat"""
    chat = get_object_or_404(PharmacistChat, id=chat_id, user=request.user)
    
    # Mark messages from pharmacist as read
    chat.messages.filter(is_from_pharmacist=True, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            try:
                # Save user message
                message = form.save(commit=False)
                message.chat = chat
                message.sender = request.user
                message.is_from_pharmacist = False
                message.save()
                
                # Update chat status
                if chat.status == 'closed':
                    chat.status = 'open'
                    chat.save()
                
                # Generate automatic pharmacist response
                try:
                    auto_response = generate_pharmacist_response(message.message, chat)
                    
                    if auto_response:
                        # Get or create pharmacist user
                        from django.contrib.auth import get_user_model
                        User = get_user_model()
                        pharmacist_user, created = User.objects.get_or_create(
                            username='pharmacist_demo',
                            defaults={
                                'first_name': 'Demo',
                                'last_name': 'Pharmacist',
                                'email': 'pharmacist@pharmazone.com',
                                'is_staff': True
                            }
                        )
                        
                        # Assign pharmacist if not already assigned
                        if not chat.pharmacist:
                            chat.pharmacist = pharmacist_user
                            chat.status = 'in_progress'
                            chat.save()
                        
                        # Create pharmacist response
                        ChatMessage.objects.create(
                            chat=chat,
                            sender=pharmacist_user,
                            message=auto_response,
                            is_from_pharmacist=True
                        )
                        
                except Exception as e:
                    # If auto-response fails, create a simple fallback response
                    print(f"Auto-response error: {str(e)}")
                    
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    pharmacist_user, created = User.objects.get_or_create(
                        username='pharmacist_demo',
                        defaults={
                            'first_name': 'Demo',
                            'last_name': 'Pharmacist',
                            'email': 'pharmacist@pharmazone.com',
                            'is_staff': True
                        }
                    )
                    
                    fallback_response = f"""Thank you for your question: "{message.message}"

I'm here to help! Could you please provide a bit more detail about:
• What specific symptoms you're experiencing
• Any medicines you're asking about
• Your age (helps with dosage recommendations)

I can help with:
• Medicine dosages and usage
• Treatment for common symptoms
• Side effects and safety
• When to see a doctor

What specific information do you need?"""
                    
                    ChatMessage.objects.create(
                        chat=chat,
                        sender=pharmacist_user,
                        message=fallback_response,
                        is_from_pharmacist=True
                    )
                
                return redirect('pharmacist_chat:chat_detail', chat_id=chat.id)
                
            except Exception as e:
                messages.error(request, f'Error sending message: {str(e)}')
                return redirect('pharmacist_chat:chat_detail', chat_id=chat.id)
    else:
        form = ChatMessageForm()
    
    messages_list = chat.messages.all().order_by('created_at')
    
    context = {
        'chat': chat,
        'messages': messages_list,
        'form': form,
    }
    return render(request, 'pharmacist_chat/chat_detail.html', context)


def generate_pharmacist_response(user_message, chat):
    """Generate simple, friendly pharmacist response for any question"""
    message_lower = user_message.lower()
    
    # Get chat history for context
    previous_messages = chat.messages.filter(is_from_pharmacist=False).values_list('message', flat=True)
    chat_history = ' '.join(previous_messages).lower()
    
    # Greeting responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good evening', 'namaste']):
        return "Hello! I'm your friendly pharmacist. I'm here to help you with any questions about medicines or health. What can I help you with today?"
    
    # Thank you responses
    if any(word in message_lower for word in ['thank you', 'thanks', 'dhanyabad', 'appreciate']):
        return "You're very welcome! I'm happy to help. Feel free to ask me anything else about medicines or your health anytime."
    
    # FEVER related questions
    if any(word in message_lower for word in ['fever', 'jworo', 'temperature', 'hot body']):
        if any(word in message_lower for word in ['medicine', 'tablet', 'what to take']):
            return """For fever, you can take:

• **Paracetamol** - 1 tablet (500mg) every 6 hours
• **Maximum 4 tablets per day**
• Take with water after eating food

**Other things to do:**
• Drink lots of water
• Rest and sleep
• Use wet cloth on forehead
• Wear light clothes

**See a doctor if:**
• Fever is very high (above 103°F)
• Fever for more than 3 days
• Severe headache or body pain

What's your age? This helps me give better advice."""
        else:
            return """Fever symptoms include:
• Body feels hot
• Shivering and chills
• Headache
• Body pain and weakness
• Not feeling hungry
• Feeling tired

**Normal body temperature:** 98.6°F (37°C)
**Fever:** Above 100.4°F (38°C)

Do you want to know what medicine to take for fever?"""
    
    # HEADACHE related questions
    if any(word in message_lower for word in ['headache', 'head pain', 'migraine', 'tauko dukhyo']):
        return """For headache relief:

**Medicines you can take:**
• **Paracetamol** - 1 tablet (500mg) every 6 hours
• **Ibuprofen** - 1 tablet (400mg) every 8 hours
• Take with food and water

**Simple home remedies:**
• Rest in a quiet, dark room
• Put cold cloth on forehead
• Drink plenty of water
• Gentle head massage
• Get enough sleep

**See a doctor if:**
• Very severe sudden headache
• Headache with fever and neck stiffness
• Headaches happening often

How severe is your headache - mild, moderate, or severe?"""
    
    # COUGH related questions
    if any(word in message_lower for word in ['cough', 'khoki', 'throat', 'sore throat']):
        return """For cough treatment:

**Dry cough (no phlegm):**
• Cough syrup with Dextromethorphan
• Honey with warm water
• Steam inhalation (hot water vapor)

**Wet cough (with phlegm):**
• Cough syrup with Bromhexine
• Drink warm water frequently
• Don't take dry cough medicine

**Home remedies:**
• Warm salt water gargling
• Ginger tea with honey
• Stay hydrated

**See a doctor if:**
• Cough with blood
• High fever with cough
• Cough for more than 2 weeks

Is your cough dry or do you cough up phlegm?"""
    
    # STOMACH problems
    if any(word in message_lower for word in ['stomach', 'acidity', 'gas', 'indigestion', 'pet dukhyo', 'heartburn']):
        return """For stomach problems:

**Acidity/Heartburn:**
• **ENO** or **Gelusil** - 1 packet in water
• **Omeprazole** - 1 tablet before breakfast (for frequent acidity)
• Avoid spicy and oily food

**Gas/Bloating:**
• **Simethicone** tablets
• Drink warm water
• Light walking after meals

**General stomach upset:**
• **ORS** - 1 packet in 1 liter water
• Eat simple food (rice, banana, toast)
• Avoid milk and spicy food

**See a doctor if:**
• Severe stomach pain
• Blood in vomit
• Pain for more than 2 days

What type of stomach problem do you have - acidity, gas, or pain?"""
    
    # COLD and FLU
    if any(word in message_lower for word in ['cold', 'flu', 'runny nose', 'blocked nose', 'sneezing']):
        return """For cold and flu:

**Medicines:**
• **Paracetamol** - for fever and body pain
• **Cetirizine** - for runny nose and sneezing
• **Nasal drops** - for blocked nose

**Home remedies:**
• Steam inhalation 2-3 times daily
• Warm salt water gargling
• Drink warm liquids (tea, soup)
• Get plenty of rest
• Eat nutritious food

**Prevention:**
• Wash hands frequently
• Avoid crowded places
• Wear mask if needed

**See a doctor if:**
• High fever for more than 3 days
• Difficulty breathing
• Severe throat pain

How many days have you had these symptoms?"""
    
    # PAIN related questions
    if any(word in message_lower for word in ['pain', 'ache', 'hurt', 'dukhyo', 'body pain']):
        return """For pain relief:

**General pain medicine:**
• **Paracetamol** - 1 tablet (500mg) every 6 hours
• **Ibuprofen** - 1 tablet (400mg) every 8 hours
• Always take with food

**For different types of pain:**
• **Muscle pain** - Apply pain relief gel + take tablet
• **Joint pain** - Ibuprofen works better
• **Tooth pain** - See dentist + take paracetamol
• **Back pain** - Rest + pain medicine + hot compress

**Important:**
• Don't take more than recommended dose
• Don't take on empty stomach
• Stop if you get stomach upset

**See a doctor if:**
• Very severe pain
• Pain not getting better in 3 days
• Pain with fever

Where exactly is your pain and how severe is it?"""
    
    # DOSAGE questions
    if any(word in message_lower for word in ['dosage', 'dose', 'how much', 'how many', 'kati ota']):
        if 'paracetamol' in message_lower:
            return """Paracetamol dosage:

**Adults (18+ years):**
• 1-2 tablets (500mg each) every 6 hours
• Maximum 8 tablets per day
• Take with water after food

**Children:**
• 6-12 years: Half tablet every 6 hours
• 2-6 years: Quarter tablet every 6 hours
• Under 2 years: Ask doctor first

**Important:**
• Don't exceed maximum dose
• Take with food to avoid stomach upset
• Space doses at least 4 hours apart

How old are you? This helps me give exact dosage."""
        
        elif 'ibuprofen' in message_lower:
            return """Ibuprofen dosage:

**Adults:**
• 1 tablet (400mg) every 8 hours
• Maximum 3 tablets per day
• Always take with food

**Children over 6 months:**
• Ask doctor for exact dose based on weight

**Don't take if you have:**
• Stomach ulcers
• Heart problems
• Kidney problems
• Asthma (some people)

**Important:**
• Always take with food
• Don't take on empty stomach
• Stop if stomach upset occurs

Do you have any of these health conditions?"""
        
        else:
            return """I can help you with dosage information!

**Please tell me:**
• Which medicine are you asking about?
• Your age (helps determine correct dose)
• Any health conditions you have

**Common medicines I can help with:**
• Paracetamol (fever, pain)
• Ibuprofen (pain, inflammation)
• Cetirizine (allergy, cold)
• Omeprazole (acidity)
• Cough syrups

What specific medicine do you need dosage information for?"""
    
    # SIDE EFFECTS questions
    if any(word in message_lower for word in ['side effect', 'reaction', 'allergy', 'problem after taking']):
        return """About medicine side effects:

**Common mild side effects:**
• Stomach upset or nausea
• Drowsiness or dizziness
• Mild skin rash
• Headache

**What to do for mild side effects:**
• Take medicine with food
• Drink plenty of water
• Rest if feeling dizzy

**Stop medicine immediately if:**
• Severe skin rash or itching
• Difficulty breathing
• Severe stomach pain
• Vomiting repeatedly
• Swelling of face or throat

**Get emergency help for:**
• Can't breathe properly
• Severe allergic reaction
• Loss of consciousness

**Which medicine are you taking and what symptoms are you having?**

This helps me give you better advice about what to do."""
    
    # PREGNANCY related
    if any(word in message_lower for word in ['pregnant', 'pregnancy', 'garbhavati', 'expecting']):
        return """Medicine during pregnancy:

**Generally SAFE:**
• Paracetamol (normal dose)
• Some antibiotics (as prescribed by doctor)
• Iron and folic acid tablets
• Calcium supplements

**Generally AVOID:**
• Ibuprofen (especially last 3 months)
• Aspirin
• Most herbal medicines
• Medicines not prescribed by doctor

**Important:**
• Always tell your doctor you're pregnant
• Don't take any medicine without asking doctor first
• Even safe medicines should be taken in correct dose

**Which medicine are you asking about?**

I can tell you if it's generally safe, but always confirm with your doctor."""
    
    # CHILDREN related
    if any(word in message_lower for word in ['child', 'baby', 'kid', 'bachcha', 'years old']):
        return """Medicine for children:

**Important points:**
• Children need different doses than adults
• Many adult medicines are not safe for children
• Always use children's formulations when available

**Safe medicines for children:**
• Paracetamol syrup/drops (any age)
• Ibuprofen syrup (over 6 months)
• ORS for loose motions
• Saline drops for nose

**Never give children:**
• Adult tablets (unless doctor says)
• Aspirin (under 16 years)
• Cough medicines (under 2 years)

**For dosage:**
• Tell me child's age and weight
• I'll give exact amount to give

**How old is the child and what problem are they having?**"""
    
    # DIABETES related
    if any(word in message_lower for word in ['diabetes', 'sugar', 'blood sugar', 'chini rog']):
        return """About diabetes and medicines:

**If you have diabetes:**
• Some medicines can affect blood sugar
• Always tell pharmacist/doctor you have diabetes
• Check blood sugar regularly
• Take diabetes medicine on time

**Medicines generally safe:**
• Paracetamol (normal dose)
• Most antibiotics
• Blood pressure medicines

**Be careful with:**
• Cough syrups (may contain sugar)
• Steroids (can increase sugar)
• Some pain medicines

**Important:**
• Don't skip diabetes medicines
• Eat regular meals
• Monitor blood sugar when sick

**What medicine are you asking about?**
I can tell you if it's safe with diabetes."""
    
    # BLOOD PRESSURE related
    if any(word in message_lower for word in ['blood pressure', 'bp', 'hypertension', 'high bp']):
        return """About blood pressure and medicines:

**If you have high BP:**
• Take BP medicine regularly
• Don't stop suddenly
• Check BP regularly
• Limit salt in food

**Medicines to be careful with:**
• Some pain medicines (like ibuprofen)
• Cold medicines with decongestants
• Some herbal medicines

**Generally safe:**
• Paracetamol
• Most antibiotics
• Prescribed medicines

**Important:**
• Tell every doctor about your BP medicines
• Don't take new medicines without asking
• Monitor BP when taking new medicines

**What medicine are you asking about?**
I can tell you if it's safe with high blood pressure."""
    
    # MEDICINE INTERACTIONS
    if any(word in message_lower for word in ['together', 'with', 'same time', 'interaction', 'combine']):
        return """About taking medicines together:

**Some medicines don't mix well:**
• Can make each other stronger or weaker
• Can cause side effects
• Can be dangerous sometimes

**Common interactions:**
• Blood thinners + Aspirin = bleeding risk
• Some antibiotics + Antacids = less effective
• Heart medicines + Some pain medicines = problems

**To be safe:**
• Tell me all medicines you're taking
• Include vitamins and herbal products
• Mention any health conditions

**What medicines do you want to take together?**

List all of them and I'll tell you if it's safe or if you need to space them out."""
    
    # GENERAL HEALTH questions
    if any(word in message_lower for word in ['healthy', 'prevention', 'avoid getting sick', 'immunity']):
        return """To stay healthy:

**Good habits:**
• Eat nutritious food (fruits, vegetables)
• Drink 8-10 glasses of water daily
• Exercise regularly (even walking is good)
• Get 7-8 hours sleep
• Wash hands frequently

**Boost immunity:**
• Vitamin C (citrus fruits, amla)
• Vitamin D (sunlight, supplements)
• Zinc supplements
• Balanced diet

**Avoid:**
• Smoking and tobacco
• Too much alcohol
• Junk food regularly
• Stress (try meditation)

**Regular check-ups:**
• Blood pressure
• Blood sugar
• Cholesterol
• Weight monitoring

**Any specific health concern you want to prevent or improve?**"""
    
    # EMERGENCY situations
    if any(word in message_lower for word in ['emergency', 'urgent', 'severe', 'can\'t breathe', 'chest pain', 'unconscious']):
        return """🚨 **This sounds serious!**

**Go to hospital immediately if:**
• Can't breathe properly
• Severe chest pain
• Unconscious or very confused
• Severe bleeding
• Very high fever with neck stiffness
• Severe allergic reaction (swelling, rash)

**Call ambulance or go to nearest hospital NOW**

**For less urgent problems:**
• Visit nearest clinic
• Call your family doctor
• Go to pharmacy for advice

**Is this an emergency right now?**
If yes, please get medical help immediately and don't wait for my response."""
    
    # GENERAL medicine questions
    if any(word in message_lower for word in ['medicine', 'tablet', 'syrup', 'capsule', 'ausadhi']):
        return """I can help you with any medicine questions!

**Common things I help with:**
• What medicine to take for symptoms
• How much to take (dosage)
• When to take (timing)
• Side effects to watch for
• Can you take medicines together
• Safe for pregnancy/children

**Popular medicines I know about:**
• Paracetamol (fever, pain)
• Ibuprofen (pain, swelling)
• Cetirizine (allergy, cold)
• Omeprazole (acidity)
• Antibiotics (infections)
• Cough syrups
• Vitamins

**What specific medicine question do you have?**
Tell me the medicine name or your symptoms."""
    
    # AGE-related questions
    if any(word in message_lower for word in ['age', 'years old', 'months old', 'elderly', 'old person']):
        return """Age is important for medicine dosage!

**Different ages need different doses:**
• **Babies (0-2 years):** Special baby medicines only
• **Children (2-12 years):** Child doses, usually syrups
• **Teenagers (12-18 years):** Usually adult dose but check
• **Adults (18-65 years):** Standard adult doses
• **Elderly (65+ years):** Sometimes need lower doses

**Tell me:**
• How old are you (or the person taking medicine)?
• What medicine or symptom?

**This helps me give you the exact right amount to take safely.**

Age-appropriate dosing is very important for safety and effectiveness."""
    
    # TIMING questions
    if any(word in message_lower for word in ['when to take', 'timing', 'before food', 'after food', 'morning', 'night']):
        return """Medicine timing is important:

**Before food (empty stomach):**
• Some antibiotics
• Omeprazole (acidity medicine)
• Iron tablets

**After food:**
• Paracetamol
• Ibuprofen
• Most pain medicines
• Vitamins

**Anytime:**
• Cetirizine (allergy)
• Most cough syrups

**Morning:**
• Blood pressure medicines
• Diabetes medicines
• Vitamins

**Night:**
• Some allergy medicines (make sleepy)
• Some antibiotics

**Which medicine are you asking about?**
I'll tell you the best time to take it for maximum benefit."""
    
    # COST/PRICE questions
    if any(word in message_lower for word in ['price', 'cost', 'expensive', 'cheap', 'generic']):
        return """About medicine prices:

**Generic vs Brand:**
• Generic medicines have same active ingredient
• Much cheaper than branded medicines
• Work exactly the same way
• Government approved and safe

**To save money:**
• Ask for generic versions
• Buy larger quantities (if you use regularly)
• Compare prices at different pharmacies
• Look for pharmacy discount schemes

**We offer:**
• Both generic and branded medicines
• Competitive prices
• Free delivery over Rs. 2000
• Genuine medicines only

**Which medicine are you looking for?**
I can suggest good generic alternatives to save money."""
    
    # STORAGE questions
    if any(word in message_lower for word in ['store', 'storage', 'keep', 'expire', 'expiry']):
        return """How to store medicines properly:

**General storage:**
• Cool, dry place
• Away from direct sunlight
• Keep in original packaging
• Away from children's reach

**Refrigerator medicines:**
• Some syrups and injections
• Check label for "store in refrigerator"
• Don't freeze

**Don't store in:**
• Bathroom (too humid)
• Car (too hot)
• Kitchen (heat and moisture)

**Expiry dates:**
• Never use expired medicines
• Check date before taking
• Dispose safely after expiry

**Which medicine are you asking about storage for?**
Some have special storage requirements."""
    
    # DEFAULT response for any other question
    else:
        return f"""I'm here to help with your question: "{user_message}"

**I can help you with:**
• Medicine information and dosages
• Treatment for common symptoms (fever, headache, cough, stomach problems)
• Side effects and safety
• Medicine interactions
• Pregnancy and children's medicines
• When to see a doctor

**To give you the best answer, please tell me:**
• Your age (helps with dosage)
• Any health conditions you have
• Other medicines you're taking
• How severe is your problem

**Feel free to ask me anything about:**
• What medicine to take
• How much to take
• When to take it
• Any concerns about medicines

What specific information do you need?"""


@login_required
def my_chats(request):
    """List user's chats"""
    chats = PharmacistChat.objects.filter(user=request.user).order_by('-updated_at')
    
    context = {
        'chats': chats,
    }
    return render(request, 'pharmacist_chat/my_chats.html', context)


@login_required
def close_chat(request, chat_id):
    """Close a chat"""
    chat = get_object_or_404(PharmacistChat, id=chat_id, user=request.user)
    
    if chat.status != 'closed':
        chat.status = 'closed'
        chat.closed_at = timezone.now()
        chat.save()
        
        # Add closing message
        ChatMessage.objects.create(
            chat=chat,
            sender=request.user,
            message="Thank you for your help! This chat is now closed.",
            is_from_pharmacist=False
        )
        
        messages.success(request, 'Chat has been closed. Thank you!')
    
    return redirect('pharmacist_chat:my_chats')


def quick_response_detail(request, response_id):
    """View a quick response"""
    response = get_object_or_404(QuickResponse, id=response_id, is_active=True)
    
    context = {
        'response': response,
    }
    return render(request, 'pharmacist_chat/quick_response.html', context)


# Pharmacist views (for staff)
@login_required
def pharmacist_dashboard(request):
    """Dashboard for pharmacists"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('pharmacist_chat:home')
    
    # Get chats assigned to this pharmacist or unassigned
    open_chats = PharmacistChat.objects.filter(
        Q(status='open') | Q(status='in_progress'),
        Q(pharmacist=request.user) | Q(pharmacist__isnull=True)
    ).order_by('-updated_at')
    
    context = {
        'open_chats': open_chats,
    }
    return render(request, 'pharmacist_chat/pharmacist_dashboard.html', context)


@login_required
def pharmacist_chat_detail(request, chat_id):
    """Pharmacist view of chat"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('pharmacist_chat:home')
    
    chat = get_object_or_404(PharmacistChat, id=chat_id)
    
    # Assign chat to this pharmacist if not assigned
    if not chat.pharmacist:
        chat.pharmacist = request.user
        chat.status = 'in_progress'
        chat.save()
    
    # Mark messages from customer as read
    chat.messages.filter(is_from_pharmacist=False, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.is_from_pharmacist = True
            message.save()
            
            # Update chat status
            chat.status = 'in_progress'
            chat.save()
            
            return redirect('pharmacist_chat:pharmacist_chat_detail', chat_id=chat.id)
    else:
        form = ChatMessageForm()
    
    messages_list = chat.messages.all().order_by('created_at')
    
    context = {
        'chat': chat,
        'messages': messages_list,
        'form': form,
    }
    return render(request, 'pharmacist_chat/pharmacist_chat_detail.html', context)