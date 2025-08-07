from django import forms

from .models import Benefit


class BenefitForm(forms.ModelForm):
    
    class Meta:
        model = Benefit
        fields = ['benefit_type','detail', 'supporting_document']
        widgets = {
            'benefit_type': forms.TextInput(attrs={'class':'form-control'}),
            'detail': forms.Textarea(attrs={'class':'form-control'}),
            'benefit_type': forms.TextInput(attrs={'class':'form-control'}),
        }