from django.urls import path
from notifications.views import showNotifications, delete_notification

urlpatterns = [
    path('', showNotifications, name='show_notifications'),
    path('<notification_id>/delete', delete_notification, name='delete_notification'),
]