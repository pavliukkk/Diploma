# forms.py
from django import forms
from django import forms
from .models import UserProfile

class AvatarChangeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']