from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "owner")
    list_filter = ("email",)
    search_fields = ("email",)
# Register your models here.
