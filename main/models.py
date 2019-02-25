
from django.db import models
from django.contrib.auth.models import User

import uuid

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete = models.SET_NULL, null=True)
    name = models.CharField(max_length = 100)
    phone = models.BigIntegerField()
    emergency_phone = models.BigIntegerField()
    email = models.EmailField(unique = True)

    email_token = models.CharField(max_length=32, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    lat = models.DecimalField(max_digits = 10, decimal_places=6, default=0)
    long = models.DecimalField(max_digits = 10, decimal_places=6, default=0)
    is_safe = models.BooleanField(default=True, blank=True)
    email_verified = models.BooleanField(default=False, blank=True)
    device_token = models.CharField(max_length=260, null=True)


    def __str__(self):
        return self.name
