from django.contrib import admin

from eboard.clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Client._meta.fields]
    list_filter = (
        'gender',
    )
