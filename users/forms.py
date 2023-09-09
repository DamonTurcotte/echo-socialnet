from django import forms
from .models import EchoUser

class EchoUserCreationForm(forms.ModelForm):
    class Meta:
        model = EchoUser
        fields = ['username', 'password', 'bio', 'avatar']
        widgets = { 'password': forms.PasswordInput() }