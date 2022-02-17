from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from user_service import messages
import json
from django.http import JsonResponse
from users.models import *
from django.contrib.auth.models import User
from user_service.common_functions import *
from django.utils import timezone


# METHOD NAME:index 
# DESCRIPTION: This function renders the homepage
def index(request):
    return render(request, "index.html")

# METHOD NAME:create_user 
# DESCRIPTION: This function is for user creation/registration
@csrf_exempt
def create_user(request):
    try:
        req = json.loads(request.body)
        if all (key in req and req[key] for key in ["username", "password"]):
            #check if user already exists
            user_details = UserDetails.objects.filter(username = req["username"],is_deleted = False)
            if user_details.exists():
                return_object = {
                    "status": messages.FAIL,
                    "message": messages.USER_NAME_EXIST,
                }
            else:
                #save user details to db
                UserDetails.objects.create(username = req["username"],password = req["password"])
                #also storing user details in auth.models for authentication
                User.objects.create_user(req["username"],'',req["password"])
                return_object = {
                    "status": messages.SUCCESS,
                    "message": messages.USER_CREATION_SUCCESS,
                }
        else:
            #invalid request
            return_object = {
                "status": messages.FAIL,
                "message": messages.INVALID_REQUEST_OBJECT,
            }
    except (Exception) as error:
        #exception handling
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
    #declaring failed return object for reusing
    failed_return_object = {
                    "status": messages.FAIL,
                    "message": messages.LOGIN_FAILED,
                }
    try:
        req = json.loads(request.body)
        if all (key in req and req[key] for key in ["username", "password"]):
            #get ip address by request
            ip_address = get_user_ip_address(request)
            #trigger webhook to notify team
            trigger_webhook(req["username"],ip_address)
            #check if user exist
            user_details = UserDetails.objects.filter(username = req["username"],is_deleted = False)
            if user_details.exists():
                #saving record in loginhistory db
                UserLoginHistory.objects.create(username = req["username"],ip_address = ip_address,
                                                created_at = timezone.now())
                #get token pair
                token = get_jwt_token(user_details[0])
                if token:
                    return_object = {
                    "status": messages.SUCCESS,
                    "message": messages.LOGIN_SUCCESS,
                    "token":token
                    }
                else:
                    return_object = failed_return_object
            else:
                #user not present in db
                return_object = failed_return_object
        else:
            #invalid request
            return_object = {
                "status": messages.FAIL,
                "message": messages.INVALID_REQUEST_OBJECT,
            }
    except (Exception) as error:
        #exception handling
        print("error in authenticate_user", error)
        return_object = failed_return_object
    return JsonResponse(return_object, safe=False)

# METHOD NAME:authenticate_user 
# DESCRIPTION: This function is for authenticating the user
@csrf_exempt
def authenticate_user(request):
    #declaring failed return object for reusing
    failed_return_object = {
                    "status": messages.FAIL,
                    "message": messages.LOGIN_FAILED,
                }
    try:
        req = json.loads(request.body)
        if all (key in req and req[key] for key in ["username", "password"]):
            #get ip address by request
            ip_address = get_user_ip_address(request)
            #trigger webhook to notify team
            trigger_webhook(req["username"],ip_address)
            #check if user exists
            user_details = UserDetails.objects.filter(username = req["username"],is_deleted = False)
            if user_details.exists():
                token = get_jwt_token(user_details[0])
                if token:
                    return_object = {
                    "status": messages.SUCCESS,
                    "message": messages.USER_AUTHENTICATED,
                    "token":token
                    }
                else:
                    #get token failed
                    return_object = failed_return_object
            else:
                #user not present in db
                return_object = failed_return_object
        else:
            #invalid request
            return_object = {
                "status": messages.FAIL,
                "message": messages.INVALID_REQUEST_OBJECT,
            }
    except (Exception) as error:
        #exception handling
        print("error in authenticate_user", error)
        return_object = failed_return_object
    return JsonResponse(return_object, safe=False)




