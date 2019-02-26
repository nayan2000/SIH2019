
from django.db import models
from main.models import UserProfile
from django.utils import timezone


class Event(models.Model):
    admin = models.OneToOneField('main.UserProfile', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(default='NA')

    fund_goal = models.BigIntegerField(default = 0)
    is_active = models.BooleanField(default = True, blank = True)
    created_at = models.DateTimeField(default=timezone.now)
    # raised_amount = models.BigIntegerField(default = 0)

    def __str__(self):
        return self.name

    def getEventAdmin(self):
        return self.admin

    def getUserContribution(self, user_id):
        user_contribution = 0
        user_transactions = self.admin.received.filter(transfer_from__id=user_id)
        for transaction in user_transactions:
            user_contribution += transaction.amount
        return user_contribution

    def getFundRaised(self):
        event_transactions = self.admin.received.all()
        amount_raised = 0
        if event_transactions:
            for transaction in event_transactions:
                amount_raised+=transaction.amount
        return amount_raised


class Transaction(models.Model):
    transfer_to = models.ForeignKey('main.UserProfile', on_delete=models.SET_NULL, related_name = 'received', null=True)
    transfer_from = models.ForeignKey('main.UserProfile', on_delete = models.SET_NULL, related_name='sent', null=True)
    amount = models.PositiveIntegerField(default=0)
    payment_id = models.CharField(null=True, max_length=30, unique=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} from {} to {}".format(self.amount, self.transfer_from.name, self.transfer_to.name)

    def getPayerName(self):
        return self.transfer_from.name

    def getReceiverName(self):
        return self.transfer_to.name

