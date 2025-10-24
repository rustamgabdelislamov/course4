from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from clients.forms import ClientForm
from clients.models import Client



class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    paginate_by = 3


    def get_queryset(self):
        # Показываем только клиентов, созданные текущим пользователем
        return Client.objects.filter(owner=self.request.user)

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:clients_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


    def form_valid(self, form):
        """Присваиваем при создании продукта id создателя"""

        form.instance.owner = self.request.user
            # Сохраняем объект
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:clients_list')

    # permission_required = 'catalog.can_unpublish_product'

    # def get_form_class(self):
    #     user = self.request.user # Извлекает объект текущего аутентифицированного пользователя из объекта запроса (self.request), связанного с текущим представлением/контекстом. |
    #     if user == self.object.owner: # Проверяет, совпадает ли текущий user с атрибутом owner объекта, который создается автоматически при создании продукта
    #         return ProductForm #  если совпадает owner создателя, то полная форма для редактирования
    #     if user.has_perm("catalog.can_unpublish_product"): # если только через разрешение, то неполная форма
    #         return ProductModeratorForm
    #     raise PermissionDenied


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('clients:clients_list')

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


class ClientDetailView(DetailView):
    model = Client


