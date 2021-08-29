from django.contrib import admin
from notifications.models import notification

# Register your models here.

class notificationAdmin(admin.ModelAdmin):
    list_display = [ 'sender', 'user', 'notification_type']

admin.site.register(notification, notificationAdmin)

