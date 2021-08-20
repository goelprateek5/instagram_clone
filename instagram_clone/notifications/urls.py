from django.urls import path
from notifications.views import showNotifications

urlpatterns = [
    path('', showNotifications, name='show_notifications'),
]