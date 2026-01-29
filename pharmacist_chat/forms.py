from django import forms
from .models import PharmacistChat, ChatMessage


class StartChatForm(forms.ModelForm):
    class Meta:
        model = PharmacistChat
        fields = ['category', 'subject']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of your question...'
            }),
        }
        labels = {
            'category': 'What type of help do you need?',
            'subject': 'Subject',
        }


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your message here...',
                'required': True
            }),
        }
        labels = {
            'message': '',
        }