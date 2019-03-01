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

        try:
            command_name = str(command).lower()
            command = BotCommand.objects.get(name = command_name)
        except Exception:
            return JsonResponse({"message":"Invalid Command. Use !commands to see the list of commands."})
          
        response = 'Command to see ' + str(command.short_description)
        #Now decide what response to be sent for the command and set it equal to response
        return JsonResponse({"message":response})

    else:
        return JsonResponse({"message":"Requests other than POST are not Supported"})

