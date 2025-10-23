from django.db import models
from users.models import CustomUser


class Letter(models.Model):
    topic_letter = models.CharField(
        unique=True,
        max_length=100,
        verbose_name="Тема сообщения",
        help_text="Введите тему сообщения",
    )
    body_letter = models.TextField(verbose_name='Сообщение', help_text='Введите сообщение')
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='letter_owners'
    )

    def __str__(self):
        return f"{self.topic_letter} "
