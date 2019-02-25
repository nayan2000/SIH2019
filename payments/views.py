from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.urls import reverse

from django.http import HttpResponse, JsonResponse

import json
import requests

from main.models import UserProfile
from payments.models import Event, Transaction

from instamojo_wrapper import Instamojo

from sih.keyconfig import *

# if SERVER:
# 	api = Instamojo(api_key=INSTA_API_KEY, auth_token=AUTH_TOKEN)
# else:
api = Instamojo(api_key=INSTA_API_KEY_test, auth_token=AUTH_TOKEN_test, endpoint='https://test.instamojo.com/api/1.1/') 


@csrf_exempt
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

@csrf_exempt
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

        purpose = 'Donating for Event:'+ str(event_id)
        response = api.payment_request_create(
            amount=str(amount),
            purpose=purpose,
            send_email=False,
            email=user_profile.email,
            buyer_name=user_profile.name,
            phone=user_profile.phone,
            redirect_url=request.build_absolute_uri(reverse("payments:payment_response"))
        )
        return JsonResponse({"url":response['payment_request']['longurl'], "status":1})

    if request.method == "GET":
        return JsonResponse({"message":"API endpoint for processing payment requests."})

def payment_response(request):

    data = request.GET
    payid=str(data['payment_request_id'])
    # try:
    #     headers = {'X-Api-Key': kINSTA_API_KEY, 'X-Auth-Token': AUTH_TOKEN}
    #     r = requests.get('https://www.instamojo.com/api/1.1/payment-requests/'+str(payid),headers=headers)
    # except:
    headers = {'X-Api-Key': INSTA_API_KEY_test, 'X-Auth-Token': AUTH_TOKEN_test}
    response = requests.get('https://test.instamojo.com/api/1.1/payment-requests/'+str(payid), headers=headers)
    
    json_ob = response.json()
    payment_status = json_ob['success']

    if not payment_status:
        return JsonResponse({"message":'Transaction failed!', "status":0})
    
    else:
        payment_request = json_ob['payment_request']
        purpose = payment_request['purpose']
        event_id = int(purpose.split(':')[1])
        amount = int(float(payment_request['amount']))
        email = payment_request["email"]
        payment_id=json_ob['payment_request']['payments'][0]['payment_id']

        event = Event.objects.get(id=event_id)
        transfer_from = UserProfile.objects.get(email=email)
        transfer_to = event.admin

        transaction, created = Transaction.objects.get_or_create(amount=amount, transfer_from=transfer_from, transfer_to=transfer_to, payment_id=payment_id)
        return JsonResponse({"message":'Transaction Successful!', "status":1})
