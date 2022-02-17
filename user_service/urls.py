from django.contrib import admin
from django.urls import path,include
from users.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),#admin portal
    path('', index, name='index'),#home page
    path('api/user-service/create-user', create_user, name='create_user'),#create user api
    path('api/user-service/authenticate-user', authenticate_user, name='authenticate_user'),#user authentication api
    path('api/user-service/user-login', user_login, name='user_login'),#user login api
    path('', include('social_django.urls', namespace='social')),#social urls
    path('logout', auth_views.LogoutView.as_view(template_name="index.html"), name='logout'),#social logout

]
