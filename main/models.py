
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete = models.SET_NULL, null=True)
    name = models.CharField(max_length = 100)
    phone = models.BigIntegerField()
    emergency_phone = models.BigIntegerField()
    email = models.EmailField(unique = True)
    lat = models.DecimalField(max_digits = 10, decimal_places=6, default=0)
    long = models.DecimalField(max_digits = 10, decimal_places=6, default=0)
    is_safe = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.name
