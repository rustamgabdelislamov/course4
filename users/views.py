from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView

from dotenv import load_dotenv

from clients.models import Client
from mailing.models import Mailing
from users.forms import CustomUserCreationForm, CustomUserManagerForm
from users.models import CustomUser, Contacts

load_dotenv()
from django.shortcuts import render


load_dotenv()

def logout_view(request):
    logout(request)
    return redirect("/")


class HomeView(TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user

        is_staff = user.is_staff
        is_manager = user.groups.filter(name='manager').exists()
        # Количество всех рассылок
        total_mailings = Mailing.objects.count()

        # Количество активных рассылок (status="started")
        active_mailings = Mailing.objects.filter(status="started").count()

        # Количество уникальных клиентов
        unique_clients = Client.objects.count()

        context.update({
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_clients': unique_clients,
            'is_manager': is_manager,
            'is_staff': is_staff,

        })
        return context


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('clients:clients_list') # pomeniat potom na glawnuyu stranicu


class UsersListView(ListView):
    model = CustomUser
    context_object_name = 'customusers_list'
    template_name = 'users/customusers_list.html'


class UsersDetailView(DetailView):
    model = CustomUser
    context_object_name = 'users'


class UsersContactsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'catalog/contacts.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        # Создаем новый объект Contact и сохраняем его в базу данных
        Contacts.objects.create(name=name, phone=phone, message=message)
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")



class UsersUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:customusers_list')

    permission_required = 'users.can_is_active'

    def get_form_class(self):
        user = self.request.user

        # Если пользователь обновляет себя, используем форму, которая не дает менять права
        if user == self.object:
            return CustomUserCreationForm

            # В противном случае (если он администратор, обновляющий другого),
        # используем форму с полными правами.
        return CustomUserManagerForm