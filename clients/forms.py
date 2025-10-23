from django import forms
from clients.models import Client
from users.forms import StyleFormMixin


class ClientForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']