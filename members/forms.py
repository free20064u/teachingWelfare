from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


from .models import Benefit
from accounts.models import CustomUser


class BenefitForm(forms.ModelForm):
    
    class Meta:
        model = Benefit
        fields = ['benefit_type','detail', 'supporting_document']
        widgets = {
            'benefit_type': forms.TextInput(attrs={'class':'form-control'}),
            'detail': forms.Textarea(attrs={'class':'form-control'}),
            'benefit_type': forms.TextInput(attrs={'class':'form-control'}),
        }


class EditProfileForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model =  CustomUser
        fields = ['first_name', 'middle_name', 'last_name','date_of_birth','phone_number', 'email','category','gender','marital_status','region','home_town','house_number']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'First Name'}),
            'middle_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Last Name'}),
            'date_of_birth': forms.DateInput(attrs={'class':'form-control shadow', 'placeholder':'Last Name', 'type':'date'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Phone number'}),
            'email': forms.EmailInput(attrs={'class':'form-control shadow', 'placeholder':'Email'}),
            'category': forms.Select(attrs={'class':'form-control shadow'}),
            'gender': forms.Select(attrs={'class':'form-control shadow'}),
            'marital_status': forms.Select(attrs={'class':'form-control shadow'}),
            'region': forms.Select(attrs={'class':'form-control shadow'}),
            'home_town': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Home town'}),
            'house_number': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'House number'}),

        }
