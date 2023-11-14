from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Client, Mailing, Message

User = get_user_model()

admin.site.register(User, UserAdmin)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(Client)
