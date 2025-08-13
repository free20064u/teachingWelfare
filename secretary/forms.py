from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'announcementTitle'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'id': 'announcementContent', 'rows': 3}),
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
        }