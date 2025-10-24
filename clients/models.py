from django.db import models
from users.models import CustomUser

class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите email')
    full_name = models.CharField(
        max_length=100,
        verbose_name="Ф.И.О клиента",
        help_text="Введите Ф.И.О клиента",
    )
    comment = models.TextField(verbose_name='Комментарий', help_text='Введите комментарий')
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='owners'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активность",
        blank=True,
        null=True,
    )
    def __str__(self):
        return f"{self.email} {self.full_name}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = [
            "email",
        ]


