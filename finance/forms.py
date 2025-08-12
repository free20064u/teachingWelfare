from django import forms
from .models import Dues


class DuesPaymentForm(forms.ModelForm):
    class Meta:
        model = Dues
        fields = ['amount', 'payment_date', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_date'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
