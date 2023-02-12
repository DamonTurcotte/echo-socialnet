from django import forms
from .models import PvtMessage
    

class CreatePvtMessageForm(forms.ModelForm):
    class Meta:
        model = PvtMessage
        fields = ['chat', 'sender', 'receiver', 'message']
