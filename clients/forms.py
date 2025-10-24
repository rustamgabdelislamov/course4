from django import forms
from clients.models import Client
from users.forms import StyleFormMixin


class ClientForm(StyleFormMixin,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['email'].queryset = Client.objects.filter(owner=user)
        self.fields['full_name'].queryset = Client.objects.filter(owner=user)
        self.fields['comment'].queryset = Client.objects.filter(owner=user)

    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']