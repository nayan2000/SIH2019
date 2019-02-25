from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json
import requests

from main.models import UserProfile
from payments.models import Event, Transaction

# from instamojo_wrapper import Instamojo

def get_all_events(request):
    events =  Event.objects.all().values('name', 'description','fund_goal' )
    return JsonResponse({"events":list(events)})