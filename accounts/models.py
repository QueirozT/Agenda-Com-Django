from captcha.fields import CaptchaField
from django import forms
from django.db import models

from contatos.models import Contato


class ContatoForm(forms.ModelForm):
    captcha = CaptchaField()
    
    class Meta:
        model = Contato
        exclude = ('mostrar',)
        
