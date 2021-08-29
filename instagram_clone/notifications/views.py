from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from notifications.models import notification
# Create your views here.

def showNotifications(request):
    user = request.user
    notifications = notification.objects.filter(user = user).order_by('-date')
    notifications.update(is_seen=True)
    template = loader.get_template('notifications.html')


    context = {
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))

def delete_notification(request, notification_id):
    user = request.user
    notification.objects.filter(id=notification_id, user=user).delete()
    return redirect('show_notifications')


def count_notifications(request):
    notification_count = 0
    if request.user.is_authenticated:
        notification_count = notification.objects.filter(user=request.user, is_seen=False).count()

    return {'notification_count':notification_count}