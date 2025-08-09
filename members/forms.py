from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


from .models import Benefit, Children, NextOfKin, Parent, Spouse
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


class SpouseForm(forms.ModelForm):
    class Meta:
        model =  Spouse
        fields = ['first_name', 'middle_name', 'last_name','phone_number','house_number','member']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'First Name'}),
            'middle_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Phone number'}),
            'house_number': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'House number'}),
            'member': forms.HiddenInput(),
        }


class ChildrenForm(forms.ModelForm):
    class Meta:
        model =  Children
        fields = ['first_name', 'middle_name', 'last_name','member']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'First Name'}),
            'middle_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Last Name'}),
            'member': forms.HiddenInput(),
        }


class NextOfKinForm(forms.ModelForm):
    class Meta:
        model =  NextOfKin
        fields = ['first_name', 'middle_name', 'last_name','phone_number','house_number','member']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'First Name'}),
            'middle_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Phone number'}),
            'house_number': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'House number'}),
            'member': forms.HiddenInput(),
        }


class ParentForm(forms.ModelForm):
    class Meta:
        model =  Parent
        fields = ['fathers_first_name', 'fathers_middle_name', 'fathers_last_name','mothers_first_name', 'mothers_middle_name', 'mothers_last_name','member']

        widgets = {
            'fathers_first_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'First Name'}),
            'fathers_middle_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Middle Name'}),
            'fathers_last_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Last Name'}),
            'mothers_first_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'First Name'}),
            'mothers_middle_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Middle Name'}),
            'mothers_last_name': forms.TextInput(attrs={'class':'form-control shadow', 'placeholder':'Last Name'}),
            
            'member': forms.HiddenInput(),
        }
