'''
    This file contains all the views for ChatBot feature of the app.
'''

import json

from main.models import UserProfile, BotCommand, COMMAND_CHOICES
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import JsonResponse, HttpResponse

def check_user(request):
    try:
        user_id = str(request.META['HTTP_X_USER_ID'])
    except KeyError:
        return 0, JsonResponse({"message":"Header missing: X-USER-ID", "status":2})
    try:
        user_profile = UserProfile.objects.get(uuid=user_id)
        if not user_profile:
            raise Exception
    except Exception:
        return 0, JsonResponse({"message":"The given UserId doesnt correspond to any user."})
    return 1, user_id, user_profile      

@csrf_exempt
def command_response(request):
    
    if request.method == 'POST':
        check = check_user(request)
        try:
            user_id, user_profile = check[1:]
        except ValueError:
            return check[1]
        
        try:
            # just to decode JSON properly
            data = json.loads(request.body.decode('utf8').replace("'", '"'))
        except Exception:
            return JsonResponse({"message": "Please check syntax of JSON data passed.", 'status':4})

        try:
            command = data['command']
        except KeyError as missing_data:
            return JsonResponse({"message":"Field Missing: {0}".format(missing_data), "status":3})
        command = str(command)
        send_purpose = False
        if command[0]=='?':
            send_purpose = True
            command = '!'+command[1:]
        try:
            command_name = command.lower()
            command = BotCommand.objects.get(name = command_name)
        except Exception as e:
            print(e)
            return JsonResponse({"message":"Invalid Command. Use !commands to see the list of commands.",'status':0})
        if send_purpose:
            response = command.short_description
        else:
            response = command.response
        
        #changes to be made for food and safe locations and contacts
        return JsonResponse({"message":response,'status':1})
    else:
        return JsonResponse({"message":"Requests other than POST are not Supported", 'status':0})


'''

!<command_name> gives a Smart Response.
?<command_name> gives the purpose/function of Command.

!commands would give:
Use !food to get latest Food Drop Locations.
Use !safe to get the safe locations nearby you.
Use !contact to get Emergency Contacts.
Use !donate to Donate for the people in trouble.
Use !intro to get to know more about the bot.
Use !commands to get the list of commands.

!donate would give:
To donate for the people in trouble, go to the Donate section of the app and
select a suitable amount and go ahead and pay. You're done.

!intro would give:
Hey! Myself AlertBot. I am here for your service. I am a part of the Rescue Operations Team.

'''

