from django.db import models

from clients.models import Client
from letter.models import Letter
from users.models import CustomUser


class Mailing(models.Model):
    CREATED = 'created'
    LAUNCHED = 'launched'
    COMPLETED = 'completed'

    MAILING_STATUS_CHOICES = [
        (CREATED, 'создана'),
        (LAUNCHED, 'отправлена'),
        (COMPLETED, 'завершена'),
    ]

    name_mailing = models.CharField(unique=True, max_length=150, verbose_name='Название рассылки')
    start_time = models.DateTimeField(verbose_name='Время старта', blank=True, null=True)
    end_time = models.DateTimeField(verbose_name='Время окончания', blank=True, null=True)
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='letter')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mailing_owner', verbose_name='Создатель')
    clients = models.ManyToManyField(Client, related_name='client', verbose_name='Получатель')
    status = models.CharField(max_length=9, choices=MAILING_STATUS_CHOICES, default=CREATED, verbose_name='Статус')


    def __str__(self):
        return f"{self.name_mailing}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['name_mailing', ]
        # permissions = [
        #     ('can_promote_student', 'Can promote student'),
        #     ('can_expel_student', 'Can expel student'),
        # ]


class Attempt(models.Model):
    LOG_STATUSES = [
        ('sending', 'Отправляется'),
        ('delivered', 'Доставлено'),
        ('failed', 'Ошибка отправки'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=LOG_STATUSES, default='sending')
    response_message = models.TextField(blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing', verbose_name='Рассылка')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attempt_owner', verbose_name='Создатель')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='attempts', verbose_name='Получатель')
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активность",
        blank=True,
        null=True,
    )