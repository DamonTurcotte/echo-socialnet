from django import forms
from .models import EchoUser
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class EchoUserCreationForm(forms.ModelForm):
    class Meta:
        model = EchoUser
        fields = ['username', 'password', 'bio', 'avatar']
        widgets = { 'password': forms.PasswordInput() }

class EchoUserLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)