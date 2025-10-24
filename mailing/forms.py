from django import forms

from clients.models import Client
from letter.models import Letter
from mailing.models import Mailing
from users.forms import StyleFormMixin


class MailingForm(StyleFormMixin,forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=user)
        self.fields['letter'].queryset = Letter.objects.filter(owner=user)

    class Meta:
        model = Mailing
        fields = ['name_mailing', 'letter', 'clients']
