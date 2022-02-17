from ipaddress import ip_address
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from user_service import messages
import json
from django.http import JsonResponse
from users.models import *
from django.contrib.auth.models import User
from user_service.common_functions import *
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# METHOD NAME:create_user 
# DESCRIPTION: This function is for user creation/registration
@csrf_exempt
def create_user(request):
    try:
        req = json.loads(request.body)
        if all (key in req and req[key] for key in ["username", "password"]):
            user_details = UserDetails.objects.filter(username = req["username"],is_deleted = False)
            if user_details.exists():
                return_object = {
                    "status": messages.FAIL,
                    "message": messages.USER_NAME_EXIST,
                }
            else:
                UserDetails.objects.create(username = req["username"],password = req["password"])
                #also storing user details in auth.models for authentication
                User.objects.create_user(req["username"],'',req["password"])
                return_object = {
                    "status": messages.SUCCESS,
                    "message": messages.USER_CREATION_SUCCESS,
                }
        else:
            return_object = {
                "status": messages.FAIL,
                "message": messages.INVALID_REQUEST_OBJECT,
            }
    except (Exception) as error:
        print("error in create_user", error)
        return_object = {
            "status": messages.FAIL,
            "message": messages.USER_CREATION_FAIL,
        }
    return JsonResponse(return_object, safe=False)


# METHOD NAME:user_login 
# DESCRIPTION: This function is for user login
@csrf_exempt
def user_login(request):
    try:
        req = json.loads(request.body)
        if all (key in req and req[key] for key in ["username", "password"]):
            ip_address = get_user_ip_address(request)
            user_details = UserDetails.objects.filter(username = req["username"],is_deleted = False)
            if user_details.exists():
                UserLoginHistory.objects.create(username = req["username"],ip_address = ip_address,
                                                created_at = timezone.now())
                return_object = {
                    "status": messages.SUCCESS,
                    "message": messages.LOGIN_SUCCESS,
                    }
            else:
                return_object = {
                    "status": messages.FAIL,
                    "message": messages.LOGIN_FAILED,
                }
        else:
            return_object = {
                "status": messages.FAIL,
                "message": messages.INVALID_REQUEST_OBJECT,
            }
    except (Exception) as error:
        print("error in authenticate_user", error)
        return_object = {
            "status": messages.FAIL,
            "message": messages.LOGIN_FAILED,
        }
    return JsonResponse(return_object, safe=False)

# METHOD NAME:authenticate_user 
# DESCRIPTION: This function is for authenticating the user
@csrf_exempt
def authenticate_user(request):
    try:
        req = json.loads(request.body)
        failed_return_object = {
            "status": messages.FAIL,
            "message": messages.USER_AUTHENTICATION_FAIL,
        }
        if all (key in req and req[key] for key in ["username", "password"]):
            ip_address = get_user_ip_address(request)
            trigger_webhook(req["username"],ip_address)
            user_details = User.objects.filter(username = req["username"])
            if user_details.exists():
                token = get_token(user_details[0])
                if token:
                    return_object = {
                    "status": messages.SUCCESS,
                    "message": messages.USER_AUTHENTICATED,
                    "token":token
                    }
                else:
                    return_object = failed_return_object
            else:
                return_object = failed_return_object
        else:
            return_object = {
                "status": messages.FAIL,
                "message": messages.INVALID_REQUEST_OBJECT,
            }
    except (Exception) as error:
        print("error in authenticate_user", error)
        return_object = failed_return_object
    return JsonResponse(return_object, safe=False)




# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)


