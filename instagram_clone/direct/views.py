from django import template
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.shortcuts import redirect
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from direct.models import Message
from django.core.paginator import Paginator
# Create your views here.

@login_required
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = None
    directs = None
    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user = user, recepient = message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread']=0

    context = {
        'directs':directs,
        'messages':messages,
        'active_direct':active_direct,
        'user': user
    }
    template = loader.get_template('direct/direct.html')

    return HttpResponse(template.render(context, request))

@login_required
def direct(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recepient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    
    context = {
        'directs':directs,
        'messages': messages,
        'active_direct' : active_direct,
    }

    template = loader.get_template('direct/direct.html')

    return HttpResponse(template.render(context, request))

@login_required
def sendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')

    else:
        HttpResponseBadRequest()

@login_required
def userSearch(request):
    query = request.GET.get('q')
    context = {}

    if query:
        users = User.objects.filter(Q(username__icontains=query))

        #Pagination
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users':users_paginator,
        }
    template = loader.get_template('direct/search_user.html')

    return HttpResponse(template.render(context, request))

@login_required
def newConversation(request, username):
    from_user = request.user
    body = "Says Hello!"

    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('user_search')
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
    return redirect('inbox')