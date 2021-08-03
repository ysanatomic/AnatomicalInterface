from interface.serverFunctions.getPlayers import getPlayerCount
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from interface.models import Player, ServerClient
from django.shortcuts import redirect
from interface.supportFunctions.tickets import *
import threading
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
import asyncio

channel_layer = get_channel_layer()

# Create your views here.

@login_required(login_url = '/login/')
def index(request):
    return render(request, 'interface/index.html')

@login_required(login_url = '/login/')
def room(request, room_name):
    try:
        sc = ServerClient.objects.get(name=room_name)
    except:
        return redirect("index")

    return render(request, 'interface/room.html', {
        'room_name': room_name
    })

@login_required(login_url = "/login/")
def serversView(request):

    user = request.user
    profile = Player.objects.get(user=user)
    hasPermissionsTo = profile.rights_in.all()
    print(hasPermissionsTo)
    for server in hasPermissionsTo:
        print(server.is_online)
        if server.is_online:
            serverName = server.name
            ticket = createTicket() 
            # loop = asyncio.new_event_loop()
            # asyncio.set_event_loop(loop)
            to_send = {'type':'inquiry', 'inquiry': {'ticket': ticket, 'cmd': 'getOnlinePlayerCount'}}
            # loop.create_task(async_to_sync(channel_layer.group_send)(serverName + "Server", to_send))
            # event_loop = asyncio.new_event_loop()
            # event_loop.run_until_complete(channel_layer.group_send(serverName + "Server", to_send))
            # server.playerCount = event_loop.call_later(5, getTicketOutput(ticket), None)
            async_to_sync(channel_layer.group_send)(serverName + "Server", to_send)
            server.playerCount = getTicketOutput(ticket)
        else:
            server.playerCount = 0

    return render(request, 'interface/servers.html', {"servers": hasPermissionsTo})
