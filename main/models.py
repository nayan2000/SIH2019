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
    is_food_req = models.BooleanField(default=True, blank=True)
    email_verified = models.BooleanField(default=False, blank=True)
    device_token = models.CharField(max_length=260, null=True)
    is_da = models.BooleanField(default=False, blank=True)


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

COMMAND_CHOICES = (
	('!food','FOOD DROP AREAS'),
	('!safe','SAFE LOCATIONS'),
	('!contact','EMERGENCY CONTACTS'),
	('!commands', 'LIST OF COMMANDS'),
	('!intro', 'ABOUT ME'),
	('!donate', 'DONATE FOR EVENTS')
)

'''
To Create all Commands on your local server once in beginning.
Run python manage.py shell and then enter the following:

from main.models import COMMAND_CHOICES, BotCommand
for i in range(len(COMMAND_CHOICES)):
    BotCommand.objects.create(name = COMMAND_CHOICES[i][0], short_description = COMMAND_CHOICES[i][1])
'''


class BotCommand(models.Model):

    '''
        Model to store possible commands of the chatbot in the app
        Response field is kept to store responses of commands as updated by the DA
        from the web portal.
    '''

    name = models.CharField(max_length=10, unique=True)
    response = models.TextField(default='', blank=True)
    short_description = models.CharField(max_length = 150, blank=True)

    def __str__(self):
        return "Command #%d: %s" % (self.id, self.name)

    class Meta:
        verbose_name = 'Bot Command'
        verbose_name_plural = 'Bot Commands'


class UploadFile(models.Model):
    '''
        Model to store the files uploaded by the DA
    '''

    name = models.CharField(max_length=64)
    filer = models.FileField(upload_to='../media/')
