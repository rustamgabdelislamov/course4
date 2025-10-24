from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.timezone import now
from mailing.forms import MailingForm
from mailing.models import Mailing, Attempt


def send_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)

    # 1. Сменим статус на "Отправлена" и сохраним время старта
    mailing.status = Mailing.LAUNCHED
    mailing.start_time = now()
    mailing.save()

    # 2. Попытаемся отправить письма всем клиентам
    successes = 0
    failures = 0

    for client in mailing.clients.all():
        try:
            # Отправляем письмо
            send_mail(
                subject=mailing.letter.topic_letter,
                message=mailing.letter.body_letter,
                from_email='hrustam911@mail.ru',
                recipient_list=[client.email],
                fail_silently=False
            )

            # Создаем запись о доставке письма
            Attempt.objects.create(
                mailing=mailing,
                client=client,
                status='delivered',
                response_message='Письмо доставлено',
                owner=request.user
            )
            successes += 1
        except Exception as err:
            # В случае ошибки отправляем уведомление
            Attempt.objects.create(
                mailing=mailing,
                client=client,
                status='failed',
                response_message=str(err),
                owner=request.user
            )
            failures += 1

    # 3. Если все письма отправлены, меняем статус на "Завершена"
    if successes + failures == len(mailing.clients.all()):
        mailing.status = Mailing.COMPLETED
        mailing.end_time = now()
        mailing.save()

    return redirect('/')


class MailingListView(ListView):
    model = Mailing
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        is_manager = user.is_authenticated and user.groups.filter(name='manager').exists()
        queryset = Mailing.objects.all()
        if is_manager:
            # Модератор видит все рассылки
            return Mailing.objects.all().order_by('-start_time')
        else:
            # Обычный пользователь видит только свои рассылки
            return Mailing.objects.filter(owner=user).order_by('-start_time')

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        """Присваиваем при создании продукта id создателя"""

        form.instance.owner = self.request.user
            # Сохраняем объект
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    # permission_required = 'catalog.can_unpublish_product'

    # def get_form_class(self):
    #     user = self.request.user # Извлекает объект текущего аутентифицированного пользователя из объекта запроса (self.request), связанного с текущим представлением/контекстом. |
    #     if user == self.object.owner: # Проверяет, совпадает ли текущий user с атрибутом owner объекта, который создается автоматически при создании продукта
    #         return ProductForm #  если совпадает owner создателя, то полная форма для редактирования
    #     if user.has_perm("catalog.can_unpublish_product"): # если только через разрешение, то неполная форма
    #         return ProductModeratorForm
    #     raise PermissionDenied


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    # permission_required = "catalog.delete_product"

    # def get_object(self, queryset=None):
    #     """
    #     Разрешает удаление, если пользователь является владельцем ИЛИ модератором.
    #     """
    #     obj = super().get_object(queryset)
    #
    #     # Проверка 1: Является ли пользователь владельцем объекта?
    #     is_owner = (self.request.user == obj.owner)
    #
    #     # Проверка 2: Имеет ли пользователь право модератора?
    #     has_moderator_permission = self.request.user.has_perm(self.permission_required)
    #
    #     if is_owner or has_moderator_permission:
    #         return obj
    #     raise PermissionDenied


class MailingDetailView(DetailView):
    model = Mailing


class AttemptListView(ListView):
    model = Attempt
    paginate_by = 3

    def get_queryset(self):
        # Показываем только сообщения, созданные текущим пользователем
        return Mailing.objects.filter(owner=self.request.user)
