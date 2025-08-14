from django import forms
from django.core.exceptions import ValidationError
import re


from accounts.models import CustomUser
from .models import Benefit, Children, NextOfKin, Parent, Spouse


class BenefitForm(forms.ModelForm):
    """A form for creating and updating benefits."""

    class Meta:
        model = Benefit
        fields = ["benefit_type", "detail", "supporting_document", "member"]
        widgets = {
            "benefit_type": forms.Select(attrs={"class": "form-control"}),
            "detail": forms.Textarea(
                attrs={"class": "form-control", "rows": "10", "cols": "20"}
            ),
            "supporting_document": forms.FileInput(attrs={"class": "form-control"}),
            "member": forms.HiddenInput(),
        }


class EditProfileForm(forms.ModelForm):
    """A form for users to edit their profile information."""

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "phone_number",
            "email",
            "category",
            "gender",
            "marital_status",
            "region",
            "home_town",
            "house_number",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "First Name"}
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Middle Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Last Name"}
            ),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control shadow", "type": "date"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Phone number"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control shadow", "placeholder": "Email"}
            ),
            "category": forms.Select(attrs={"class": "form-control shadow"}),
            "gender": forms.Select(attrs={"class": "form-control shadow"}),
            "marital_status": forms.Select(attrs={"class": "form-control shadow"}),
            "region": forms.Select(attrs={"class": "form-control shadow"}),
            "home_town": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Home town"}
            ),
            "house_number": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "House number"}
            ),
        }

    def clean_phone_number(self):
        """Validate the phone number format."""
        phone_number = self.cleaned_data.get("phone_number", "").strip()
        if phone_number and not re.match(r"^\+?\d{9,15}$", phone_number):
            raise ValidationError(
                "Enter a valid phone number. It can start with '+' and should contain 9 to 15 digits."
            )
        return phone_number


class SpouseForm(forms.ModelForm):
    """A form for creating and updating spouse information."""

    class Meta:
        model = Spouse
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "phone_number",
            "house_number",
            "member",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "First Name"}
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Middle Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Last Name"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Phone number"}
            ),
            "house_number": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "House number"}
            ),
            "member": forms.HiddenInput(),
        }

    def clean_phone_number(self):
        """Validate the phone number format."""
        phone_number = self.cleaned_data.get("phone_number", "").strip()
        if phone_number and not re.match(r"^\+?\d{9,15}$", phone_number):
            raise ValidationError(
                "Enter a valid phone number. It can start with '+' and should contain 9 to 15 digits."
            )
        return phone_number


class ChildrenForm(forms.ModelForm):
    """A form for creating and updating children's information."""

    class Meta:
        model = Children
        fields = ["first_name", "middle_name", "last_name", "member"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "First Name"}
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Middle Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Last Name"}
            ),
            "member": forms.HiddenInput(),
        }


class NextOfKinForm(forms.ModelForm):
    """A form for creating and updating next of kin information."""

    class Meta:
        model = NextOfKin
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "phone_number",
            "house_number",
            "member",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "First Name"}
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Middle Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Last Name"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Phone number"}
            ),
            "house_number": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "House number"}
            ),
            "member": forms.HiddenInput(),
        }

    def clean_phone_number(self):
        """Validate the phone number format."""
        phone_number = self.cleaned_data.get("phone_number", "").strip()
        if phone_number and not re.match(r"^\+?\d{9,15}$", phone_number):
            raise ValidationError(
                "Enter a valid phone number. It can start with '+' and should contain 9 to 15 digits."
            )
        return phone_number


class ParentForm(forms.ModelForm):
    """A form for creating and updating parent information."""

    class Meta:
        model = Parent
        fields = [
            "fathers_first_name",
            "fathers_middle_name",
            "fathers_last_name",
            "mothers_first_name",
            "mothers_middle_name",
            "mothers_last_name",
            "member",
        ]
        widgets = {
            "fathers_first_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "First Name"}
            ),
            "fathers_middle_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Middle Name"}
            ),
            "fathers_last_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Last Name"}
            ),
            "mothers_first_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "First Name"}
            ),
            "mothers_middle_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Middle Name"}
            ),
            "mothers_last_name": forms.TextInput(
                attrs={"class": "form-control shadow", "placeholder": "Last Name"}
            ),
            "member": forms.HiddenInput(),
        }


class ProfilePictureForm(forms.ModelForm):
    """A form for updating the user's profile picture."""

    class Meta:
        model = CustomUser
        fields = ["profile_picture"]
        widgets = {
            "profile_picture": forms.FileInput(attrs={"class": "form-control"}),
        }
