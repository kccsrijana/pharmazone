from django import forms
from .models import MedicineReview, Prescription


class MedicineReviewForm(forms.ModelForm):
    """Form for medicine reviews"""
    
    class Meta:
        model = MedicineReview
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].required = True
        self.fields['title'].required = True
        self.fields['comment'].required = True


class PrescriptionUploadForm(forms.ModelForm):
    """Form for prescription uploads"""
    
    class Meta:
        model = Prescription
        fields = [
            'medicine', 'prescription_image', 'doctor_name', 
            'doctor_license', 'prescription_date', 'notes'
        ]
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'prescription_image': forms.FileInput(attrs={'class': 'form-control'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'doctor_license': forms.TextInput(attrs={'class': 'form-control'}),
            'prescription_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show prescription medicines
        self.fields['medicine'].queryset = Medicine.objects.filter(
            prescription_type__in=['prescription', 'controlled'],
            is_active=True
        )
        self.fields['medicine'].required = True
        self.fields['prescription_image'].required = True
        self.fields['doctor_name'].required = True
        self.fields['prescription_date'].required = True
