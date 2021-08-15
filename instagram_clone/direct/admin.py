from django.contrib import admin
from direct.models import Message

# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'sender', 'recepient', 'body']

admin.site.register(Message, MessageAdmin)

