from django import forms
from letter.models import Letter
from users.forms import StyleFormMixin


class LetterForm(StyleFormMixin,forms.ModelForm):

    class Meta:
        model = Letter
        fields = ['topic_letter', 'body_letter']


