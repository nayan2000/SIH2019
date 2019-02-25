from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json
import requests

from main.models import UserProfile
from payments.models import Event, Transaction

# from instamojo_wrapper import Instamojo

def get_active_events(request):

    if request.method == 'GET':

        try:
            user_id = str(request.META['HTTP_X_USER_ID'])
        except KeyError:
            return JsonResponse({"message":"Header missing: X-USER-ID", "status":2})

        try:
            user_profile = UserProfile.objects.get(uuid=user_id)
        except Exception:
            return JsonResponse({"message":"The given UserId doesnt correspond to any user."})

        events =  Event.objects.filter(is_active=True).values('name','id')
        return JsonResponse({"events":list(events)})

    elif request.method == 'POST':
        return JsonResponse({"message":"A <GET> Request only endpoint for getting details of active events."})

def get_event_details(request, event_id):
    if request.method == 'GET':

        try:
            user_id = str(request.META['HTTP_X_USER_ID'])
        except KeyError:
            return JsonResponse({"message":"Header missing: X-USER-ID", "status":2})

        try:
            user_profile = UserProfile.objects.get(uuid=user_id)
        except Exception:
            return JsonResponse({"message":"The given UserId doesnt correspond to any user."})

        event_details =  Event.objects.get(id = event_id).values('id', 'name', 'description', 'fund_goal')
        return JsonResponse({"event":list(event_details)})

    elif request.method == 'POST':
        return JsonResponse({"message":"A <GET> only Request endpoint for getting details of active events."})
