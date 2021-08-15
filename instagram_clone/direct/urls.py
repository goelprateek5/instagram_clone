from django.urls import path
from direct.views import inbox, direct, sendDirect, userSearch, newConversation

urlpatterns = [
    path('', inbox, name='inbox'),
    path('<username>', direct, name='directs'),
    path('send/', sendDirect, name='send_direct'),
    path('new/', userSearch, name='user_search'),
    path('new/<username>', newConversation, name='new_conversation'),

]