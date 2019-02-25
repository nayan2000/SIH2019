import re
import string
import requests
import json
import sendgrid
from random import choice
import uuid

from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from django.contrib.auth.models import User

from sendgrid.helpers import *
from sendgrid.helpers.mail import Mail, Content, Email

from fcm_django.models import FCMDevice

from main.models import UserProfile
from main import utils, email_body
from sih.keyconfig import SENDGRID_API_KEY, FIREBASE_API_KEY, FCM_URL

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
url = 'http://alertify.org'

@csrf_exempt
def get_location(request):
    if request.method == 'GET':
        user_profiles = UserProfile.objects.all().exclude(lat=0, long=0).values('lat','long')
        print(user_profiles)
        return JsonResponse({"location":list(user_profiles)})

def nill(request):
    return HttpResponse('nill')

@csrf_exempt
def register(request):
    
    # Why the fuck did you send a get request here?
    if request.method == 'GET':
        return JsonResponse({'status':3, 'message':'I am being kind enough by sending you a FuckOff message here.'})

    if request.method=='POST':
        try:
            # just to decode JSON properly
            data = json.loads(request.body.decode('utf8').replace("'", '"'))
        except:
            return JsonResponse({"message": "Please check syntax of JSON data passed.", 'status':4})
        try:
            # see whether all fields passed in JSON or not
            data['name']
            data['email']
            data['phone']
            data['emergency_phone']
        except KeyError as missing_data:
            return JsonResponse({"message": "Missing the following field: {}".format(missing_data), 'status':2})

        try:
            int(data['phone'])
        except:
            #phone numbers should be an integer or string only of numbers
            return JsonResponse({'status':0,'message':'Please enter a valid Phone Number.'}) 

        try:
            int(data['emergency_phone'])
        except:
            #phone numbers should be an integer or string only of numbers
            return JsonResponse({'status':0,'message':'Please enter a valid Emergency Phone Number.'})   

        if len(data['phone'])!=10:
            return JsonResponse({'status':0,'message':'Please enter a valid Phone Number.'})
        if len(data['emergency_phone'])!=10:
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
            name = ' '.join(str(data['name']).strip().split())
            profile.name = name
            profile.email = str(data['email'])
            profile.phone = int(data['phone'])
            profile.emergency_phone = int(data['emergency_phone'])
            profile.save()

            #verify email
            send_to = profile.email
            body = email_body.register()
            email_token = utils.generate_email_token(profile)
            body = body%(name, str(request.build_absolute_uri(reverse("main:nill"))) + 'email_confirm/' + email_token + '/')

            sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
            from_email = Email('register@alertify.com')
            to_email = Email(send_to)
            subject = "Email Confirmation for your account on Alertify app"
            content = Content('text/html', body)

            try:
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
            except Exception:
                profile.delete()
                return JsonResponse({'message':'Error sending email. Please try again.', 'status':0})
            
            message = "Registration successful! A confirmation link has been sent to %s. Kindly click on it to verify your email address." %(send_to)
            return JsonResponse({'message':message, 'status':1})
        except Exception:
            return JsonResponse({'message': 'Registration failed due to unknown reasons.', 'status':0})

def mail_login_creds(user_profile):
    if not user_profile.user:
        username = user_profile.name.split(' ')[0] + str(user_profile.id)
        password = ''.join(choice(chars) for i in range(8))
        user = User.objects.create_user(username=username, password=password)
        user_profile.user = user
        user_profile.save()

        send_to = user_profile.email
        name = user_profile.name
        body = email_body.login_creds()
        body = body%(name, username, password)

        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        from_email = Email('register@alertify.com')
        to_email = Email(send_to)
        subject = "Login Credentials for your account on Alertify app"
        content = Content('text/html', body)

        try:
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            if response.status_code%100!=2:
                raise Exception
        except Exception:
            user_profile.user = None
            user_profile.save()
            user.delete()
            message = "Error in mailing your login credentials. Please try again."
            return message
        
        message = "Your login credentials have been sent to {0}.".format(send_to)
        return message

# @csrf_exempt
# def sendFCM(request, title, body):
#     if request.method == 'POST':
#         try:
#             user_id = str(request.META['HTTP_X_USER_ID'])
#         except KeyError:
#             return JsonResponse({"message":"Header missing: X-USER-ID", "status":2})

#         try:
#             user_profile = UserProfile.objects.get(uuid=user_id)
#         except Exception:
#             return JsonResponse({"message":"The given UserId doesnt correspond to any user."})

#         try:
#             # just to decode JSON properly
#             data = json.loads(request.body.decode('utf8').replace("'", '"'))
#         except:
#             return JsonResponse({"message": "Please check syntax of JSON data passed.", 'status':4})


#             # data = json.loads(request.body.decode('utf8').replace("'", '"'))
#             # title = data['title']
#             # body = data['body']
#         devices = FCMDevice.objects.all()
#         devices.send_message(
#             title="TsunaNews",
#             body="What's with the Tsunami Surfing?"
#         )


# Alternate Method
def sendNotif(fcmDeviceToken, title, message):
    payload = {
     "data":{
        "title":title,
        "image":"https://firebase.google.com/images/social.png",
        "message":message,
      }, "to": fcmDeviceToken
    }
    headers={
      "Content-Type": "application/json",
      "Authorization": "key={}".format(FIREBASE_API_KEY)
      }
    url = FCM_URL
    payload = json.dumps(payload)
    print(payload)
    res = requests.post(url=url, headers=headers, data=payload)
    # json=json.dumps(payload)
    return res


def email_confirm(request,token):
    user_profile = utils.authenticate_email_token(token)
    if user_profile:
        if (not user_profile.email_verified) or (user_profile.email_verified and not user_profile.user):
            message = 'Your email has been verified.'
            mail_response = mail_login_creds(user_profile)
            message += mail_response
            context = {
                'error_heading': 'Email verified',
                'message': message,
                'url':url
            }
        else:
            # user had already verified his email
            context = {
                'error_heading': 'Email already verified',
                'message': 'Your email had been already verified. Please login into the app using your credentials.',
                'url':url
            }
    # if email verification token was wrong
    else:
        context = {
        'error_heading': "Invalid Token",
        'message': "Sorry!  Email couldn't be verified. Please try again.",
        'url':url
        }
    return render(request, 'main/message.html', context)

@csrf_exempt
def login_view(request):
    '''
    Login page
    '''

    # To do checks if user is authenticated

    if request.method == 'POST':
        try:
            # just to decode JSON properly
            data = json.loads(request.body.decode('utf8').replace("'", '"'))
        except:
            return JsonResponse({"message": "Please check syntax of JSON data passed.", 'status':4})
        username = data['username']
        password = data['password']
        user = authenticate(username = username, password = password)
        
        if user is not None:
            login(request,user)
            # print(username,password)
            try:
                user_profile = UserProfile.objects.get(user = user)
            except:
                return JsonResponse({"message":"No Profile for the given user. ARE YOU LOGGED IN AS ADMIN?", "status":0})
            unique_id = str(user_profile.uuid)
            print(unique_id)
            return JsonResponse({"message":"Logged in Successfully!", "status":1, "user_id":unique_id})
  
        else:
            print('Invalid login creds')
            return JsonResponse({'message':'Invalid Login Credentials', 'status':0})    
    elif request.method == 'GET':
        return JsonResponse({"message":"Supposed to be Login Page."})

@csrf_exempt
def update_location(request):
    if request.method=='POST':
        
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
            data['long']
            data['lat']
        except KeyError as missing_data:
            return JsonResponse({"message":"Field Missing: {0}".format(missing_data), "status":3})
        
        try:
            latitude = float(data['lat'])
        except:
            return JsonResponse({"message":'Invalid value for \'lat\'', "status":0})
        try:
            longitude = float(data['long'])
        except:
            return JsonResponse({"message":'Invalid value for \'long\'', "status":0})

        if abs(latitude)>90:
            return JsonResponse({"message":"Latitude can only be in between -90 and 90.","status":0})
        if abs(longitude)>180:
            return JsonResponse({"message":"Longitude can only be in between -180 and 180.","status":0})

        user_profile.lat = latitude
        user_profile.long = longitude
        user_profile.save()

        return JsonResponse({"message":"Successfully Updated Latitude and Longitude values.", "status":1})

    if request.method == 'GET':
        return JsonResponse({"message":"API endpoint for updation of User Latitude and Longitude."})

@csrf_exempt
def update_safe_status(request):
    
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
            is_safe = data['is_safe']
        except KeyError as missing_data:
            return JsonResponse({"message":"Field Missing: {0}".format(missing_data), "status":3})
        
        # if (len(str(is_safe)))>1:
        #     return JsonResponse({"message":"Invalid Value for is_safe. Acceptable: 0 or 1", "status":0})
        
        if str(is_safe) not in ["0","1"]:
            return JsonResponse({"message":"Invalid Value for is_safe. Pass 0 or 1", "status":0})
        
        is_safe = int(is_safe)

        if is_safe:
            user_profile.is_safe = True
        if not is_safe:
            user_profile.is_safe = False
        user_profile.save()
        
        return JsonResponse({"message":"Updated status successfully!", "status":1})

    if request.method == "GET":
        return JsonResponse({"message":"API endpoint for updating safety status"})
        

