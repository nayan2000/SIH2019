from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from main.models import UserProfile

import re
import string
import requests
import json

@csrf_exempt
def register(request):
    
    # Why the fuck did you send a get request here?
    if request.method == 'GET':
        return JsonResponse({'status':3, 'message':'Wrong place dude! This place is just for posting.'})

    if request.method=='POST':
        data = json.loads(request.body.decode('utf8').replace("'", '"'))

        if len(data['phone'])!=10:
            return JsonResponse({'status':0,'message':'Please enter a valid Phone Number.'})
        if len(data['emergency_phone'])!=10:
            return JsonResponse({'status':0,'message':'Please enter a valid Emergency Phone Number.'})
        try:
            int(data['phone'])
        except:
            return JsonResponse({'status':0,'message':'Please enter a valid Phone Number.'})  
        try:
            int(data['emergency_phone'])
        except:
            return JsonResponse({'status':0,'message':'Please enter a valid Emergency Phone Number.'})             
        
        email = data['email']
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return JsonResponse({'status':0, 'message':'Please enter a valid Email address.'})
        
        try:
            UserProfile.objects.get(email=email)
            return JsonResponse({'status':0, 'message':'This Email has already been registered. Try some other email.'})
        except:
            pass
        try:
            profile = UserProfile()
            name = ''.join(str(data['name']).strip().split())
            profile.name = name
            profile.email = str(data['email'])
            profile.phone = int(data['phone'])
            profile.emergency_phone = int(data['emergency_phone'])
            profile.save()
            return JsonResponse({'message':'Registration Successful!', 'status':1})

        except KeyError as missing_data:
            response = JsonResponse({'message':'Data is Missing: {}'.format(missing_data), 'status':2})
            return response
