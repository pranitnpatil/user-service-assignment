from django.contrib import admin
from django.urls import path
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),#admin portal
    path("", index, name="index"),#home page
    path('api/user-service/create-user', create_user, name='create_user'),#create user api
    path('api/user-service/authenticate-user', authenticate_user, name='authenticate_user'),#user authentication api
    path('api/user-service/user-login', user_login, name='user_login'),#user login api
]
