from django.contrib import admin
from .models import UserProfile, BotCommand, UploadFile

admin.site.register(UserProfile)
admin.site.register(BotCommand)
admin.site.register(UploadFile)