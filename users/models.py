from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите email')
    phone_number = models.CharField(max_length=15, verbose_name='Телефон', blank=True, null=True, help_text='Необязательное поле. Введите номер телефона')
    image = models.ImageField(upload_to='users/image', verbose_name='Фото', blank=True, null=True)
    country = models.CharField(max_length=100,  verbose_name='Страна', blank=True, null=True,  help_text='Необязательное поле. Введите страну')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Contacts(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "контакты"
        ordering = [
            "name",
        ]