from django.contrib import admin
from django.urls import path
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path('api/user-service/create-user', create_user, name='create_user'),
    path('api/user-service/authenticate-user', authenticate_user, name='authenticate_user'),
    path('api/user-service/user-login', user_login, name='user_login'),
]
