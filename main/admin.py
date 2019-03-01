from django.contrib import admin
from .models import UserProfile, BotCommand

admin.site.register(UserProfile)
admin.site.register(BotCommand)