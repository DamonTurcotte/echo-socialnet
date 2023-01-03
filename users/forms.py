from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'bio', 'avatar']
        widgets = { 'password': forms.PasswordInput() }