from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect

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
            if not user_profile:
                raise Exception
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
            if not user_profile:
                raise Exception
        except Exception:
            return JsonResponse({"message":"The given User ID doesnt correspond to any user."})

        try:
            event =  Event.objects.get(id = event_id)
        except:
            return JsonResponse({"message":"No Event corresponding to this event ID.", "status":0})
        event_details = {
            "name":event.name, 
            "id":event.id, 
            "description":event.description,
            "fund_goal":event.fund_goal,
            "fund_raised":event.getFundRaised()
        }

        return JsonResponse({"event_details":event_details, "status":1})

    elif request.method == 'POST':
        return JsonResponse({"message":"A <GET> only Request endpoint for getting details of active events."})

@csrf_exempt
def payment_request(request):

    if request.method == 'POST':

        try:
            user_id = str(request.META['HTTP_X_USER_ID'])
        except KeyError:
            return JsonResponse({"message":"Header missing: X-USER-ID", "status":2})

        try:
            user_profile = UserProfile.objects.get(uuid=user_id)
            if not user_profile:
                raise Exception
        except Exception:
            return JsonResponse({"message":"The given UserId doesnt correspond to any user."})

        try:
            # just to decode JSON properly
            data = json.loads(request.body.decode('utf8').replace("'", '"'))
        except:
            return JsonResponse({"message": "Please check syntax of JSON data passed.", 'status':4})
        
        try:
            event_id = data["event_id"]
            amount = data["amount"]
        except KeyError as missing_data:
            return JsonResponse({"message":"Field Missing: {0}".format(missing_data), "status":3})
        try:
            amount = int(amount)
        except:
            return JsonResponse({"message":"Invalid amount. Expected Numeric Input.", "status":0})      
        if amount<10:
            return JsonResponse({"message":"Minimum contribution is Rs. 10", "status":0})

        try:
            event = Event.objects.get(id = event_id)
            if not event.is_active:
                raise Exception
            admin = event.admin
            if not admin:
                raise Exception
        except:
            return JsonResponse({"message":"Invalid Event ID/Donations for this event closed.", "status":0})
        return JsonResponse({"message":"Successful Request"})


        #main payment code

    if request.method == "GET":
        return JsonResponse({"message":"API endpoint for processing payment requests."})
    
