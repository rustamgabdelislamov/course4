from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView
import os
from dotenv import load_dotenv
from users.forms import CustomUserCreationForm
from users.models import CustomUser, Contacts

load_dotenv()
from django.shortcuts import render

# Create your views here.

load_dotenv()

def logout_view(request):
    logout(request)
    return redirect("/")


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users/base.html') # pomeniat potom na glawnuyu stranicu


class UsersListView(ListView):
    model = CustomUser
    context_object_name = 'customusers_list'
    template_name = 'users/customusers_list.html'


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
