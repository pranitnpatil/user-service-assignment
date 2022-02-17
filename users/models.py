from django.contrib import admin
from django.db import models
import csv
from django.http import HttpResponse
from io import StringIO 

# MODEL NAME:UserDetails 
# DESCRIPTION: This model is used to store user details
class UserDetails(models.Model):
    username = models.CharField(max_length = 256)
    password = models.CharField(max_length = 256)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_details'
        indexes = [
            models.Index(fields=['username']), 
        ]


# MODEL NAME:UserLoginHistory 
# DESCRIPTION: This model is used to store user login history
class UserLoginHistory(models.Model):
    username = models.CharField(max_length = 256)
    ip_address = models.CharField(max_length = 256)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'user_login_history'

# METHOD NAME:UserLoginHistoryAdmin 
# DESCRIPTION: This is to add custom action for exporting csv
class UserLoginHistoryAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ('username', 'ip_address', 'created_at')
    @admin.action(description='Export Login history as csv')
    #csv export function
    def download_csv(self, request, queryset):
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(['username', 'ip_address', 'created_at'])
        for s in queryset:
            writer.writerow([s.username, s.ip_address, s.created_at])
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=login-history.csv'
        return response

