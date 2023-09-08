from django import forms
from .models import EchoUser
from captcha.fields import ReCaptchaField
from echo.settings import RECAPTCHA_PRIVATE_KEY, RECAPTCHA_PUBLIC_KEY
from captcha.widgets import ReCaptchaV3
from django.contrib.auth.forms import AuthenticationForm

class EchoUserCreationForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = EchoUser
        fields = ['username', 'password', 'bio', 'avatar']
        widgets = { 'password': forms.PasswordInput() }

class CustomAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)