from django.contrib import admin
from .models import Event, Transaction

admin.site.register(Event)
admin.site.register(Transaction)