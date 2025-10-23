from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from letter.forms import LetterForm
from letter.models import Letter


class LetterListView(ListView):
    model = Letter
    paginate_by = 3


class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterForm
    success_url = reverse_lazy('letter:letter_list')

    def form_valid(self, form):
        """Присваиваем при создании продукта id создателя"""

        form.instance.owner = self.request.user
            # Сохраняем объект
        return super().form_valid(form)


class LetterUpdateView(UpdateView):
    model = Letter
    form_class = LetterForm
    success_url = reverse_lazy('letter:letter_list')

    # permission_required = 'catalog.can_unpublish_product'

    # def get_form_class(self):
    #     user = self.request.user # Извлекает объект текущего аутентифицированного пользователя из объекта запроса (self.request), связанного с текущим представлением/контекстом. |
    #     if user == self.object.owner: # Проверяет, совпадает ли текущий user с атрибутом owner объекта, который создается автоматически при создании продукта
    #         return ProductForm #  если совпадает owner создателя, то полная форма для редактирования
    #     if user.has_perm("catalog.can_unpublish_product"): # если только через разрешение, то неполная форма
    #         return ProductModeratorForm
    #     raise PermissionDenied


class LetterDeleteView(DeleteView):
    model = Letter
    success_url = reverse_lazy('letter:letter_list')

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


class LetterDetailView(DetailView):
    model = Letter
