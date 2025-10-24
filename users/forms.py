import os
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from django.db.models import BooleanField

from users.models import CustomUser

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # Ключ (field_name) — это строка, обозначающая имя поля («title», «content», «price» и т.п.).Значение (field) — это экземпляр конкретного класса поля, например, CharField, IntegerField, BooleanField и т.д., наследующие от базового класса полей Django.
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text='Необязательное поле. Введите ваш номер телефона')
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'image','phone_number', 'country', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        return phone_number

    def clean_image(self):
        """
        Валидирует изображение на предмет правильного расширения и максимального размера файла.
        """
        image = self.cleaned_data.get('image')  # Получаем файл

        # Проверяем тип полученного объекта
        if isinstance(image, InMemoryUploadedFile):  # Проверяем, что это файл
            file_size = image.size  # Размер файла в байтах
            max_file_size = 5 * 1024 * 1024  # Максимальный размер файла (5 MB)

            # Ограничиваем максимальный размер файла
            if file_size > max_file_size:
                raise ValidationError(f'Размер файла превышает лимит ({max_file_size // (1024 * 1024)}MB)')

            # Проверяем расширение файла
            file_extension = os.path.splitext(image.name)[1].lower()  # Расширение файла
            allowed_extensions = ('.png', '.jpg')  # Разрешённые расширения

            if file_extension not in allowed_extensions:
                raise ValidationError(f'Можно загружать только файлы формата {", ".join(allowed_extensions)}')

        return image


class CustomUserManagerForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['is_active']