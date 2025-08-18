from django import forms
from .models import Dues
from members.models import Benefit


class DuesPaymentForm(forms.ModelForm):
    class Meta:
        model = Dues
        fields = ['amount', 'payment_date', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 20.00'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes about the payment...'}),
        }


class HonourBenefitForm(forms.ModelForm):
    """
    A form for confirming or editing the amount of a benefit before honouring it.
    """
    class Meta:
        model = Benefit
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'amount': 'Honour Amount (GH₵)'
        }