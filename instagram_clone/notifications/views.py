from django import template
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from notifications.models import notification
# Create your views here.

def showNotifications(request):
    user = request.user
    notifications = notification.objects.filter(user = user).order_by('-date')

    template = loader.get_template('notifications.html')

    context = {
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))