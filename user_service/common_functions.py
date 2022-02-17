import json
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken 
from user_service import config
import requests

session = requests.Session()

# METHOD NAME:get_token 
# DESCRIPTION: This function is to get simple token
def get_token(user):
    try:
        #get/create token
        token = Token.objects.get_or_create(user=user)[0]
        if token:
            return str(token)
        else:
            return False
        
    except (Exception) as error:
        #exception handling
        print("error in get_token", error)
        return False

# METHOD NAME:get_jwt_token 
# DESCRIPTION: This function is to get JWT token
def get_jwt_token(user):
    try:
        #get jwt token pair with user_id
        token = RefreshToken.for_user(user)
        if token:
            return {
                'refresh': str(token),
                'access': str(token.access_token),
            }
        else:
            return False
        
    except (Exception) as error:
        #exception handling
        print("error in get_token", error)
        return False

# METHOD NAME:trigger_webhook 
# DESCRIPTION: This function is to trigger webhook to send ip address
def trigger_webhook(username,ip_address):
    try:
        request_dict = { 
                  'user' : username,
                  'ip' : ip_address
               }
        #sending a post request to trigger webhook
        status = session.post(config.WEBHOOK_URL, headers=config.HEADER, data=json.dumps(request_dict))
        #printing status just in case
        print("Webhook status",status.content)
    except (Exception) as error:
        #exception handling
        print("error in trigger_webhook", error)


# METHOD NAME:visitor_ip_address 
# DESCRIPTION: This function is to get users ip address
def get_user_ip_address(request):
    try:
        #getting ip address from request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except (Exception) as error:
        #exception handling
        print("error in get_user_ip_address", error)
        return "Not found"


