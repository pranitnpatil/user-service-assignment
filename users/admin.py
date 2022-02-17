import imp
from django.contrib import admin
from users.models import *
# Register your models here.
admin.site.register(UserDetails)
admin.site.register(UserLoginHistory, UserLoginHistoryAdmin)