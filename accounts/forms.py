from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from . import models


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password Confirm',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'middle_name', 'last_name','phone_number', 'email','category','gender','marital_status','region']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'middle_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }

class EditUserForm(UserChangeForm):
    password = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model =  models.CustomUser
        fields = ['first_name', 'middle_name', 'last_name','phone_number', 'email','category','gender','marital_status','region']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'middle_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone number'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'marital_status': forms.Select(attrs={'class':'form-control'}),
            'region': forms.Select(attrs={'class':'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'autofocus': True}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

