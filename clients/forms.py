import os

from django import forms
from django.db.models import BooleanField
from clients.models import Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # Ключ (field_name) — это строка, обозначающая имя поля («title», «content», «price» и т.п.).Значение (field) — это экземпляр конкретного класса поля, например, CharField, IntegerField, BooleanField и т.д., наследующие от базового класса полей Django.
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']