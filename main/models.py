from django.db import models
from django.contrib.auth.models import User

import uuid

class UserProfile(models.Model):

    '''
        This model contains all details of a user including phone, email, name
        and login creds. The latitude and longitude are kept here temporarily
        and will be shifted to firebase, if this project grows.
    '''
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
        return "#%d: %s" % (self.id, self.name)

    def getTotalDonation(self):
        user_transactions = self.sent.all()
        total_amount_donated = 0
        for transaction in user_transactions:
            total_amount_donated += transaction.amount
        return total_amount_donated

    def getEventDonation(self, event_id):
        #this import has to be here to avoid circular import Error
        from payments.models import Event

        user_contribution = 0
        event_admin_id = Event.objects.get(id=event_id).admin.id
        user_transactions = self.sent.filter(transfer_to__id=event_admin_id)
        for transaction in user_transactions:
            user_contribution += transaction.amount
        return user_contribution

'''
    Had to import it below to avoid issue of circular imports as UserProfile
    was needed in utils.
'''

from main import utils

class BotCommand(models.Model):

    '''
        Model to store possible commands of the chatbot in the app
        Response field is kept to store responses of commands as updated by the DA
        from the web portal.
    '''
    command_name = models.CharField(max_length=10, choices = utils.COMMAND_CHOICES, unique=True)
    command_response = models.TextField(default='', blank=True)

    def __str__(self):
        return "Command #%d: %s" % (self.id, self.command_name)
