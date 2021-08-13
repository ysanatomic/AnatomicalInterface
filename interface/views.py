from re import S
from interface.forms import AddNoteForm, Search
from django.http.response import Http404
from interface.serverFunctions.getPlayers import getPlayerCount
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from interface.models import ChatMessage, NPCPlayer, Notes, Player, ServerClient
from django.shortcuts import redirect
from interface.supportFunctions.tickets import *
import threading
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
import asyncio
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
import mysql.connector
from DivictusInterface.secret import litebansconfig
import uuid

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
    print("Has perm ", profile.checkForPermission("administrator"))
    for server in hasPermissionsTo:
        print(server.is_online)
        if server.is_online:
            serverName = server.name
            ticket = createTicket() 
            to_send = {'type':'inquiry', 'inquiry': {'ticket': ticket, 'cmd': 'getOnlinePlayerCount'}}
            async_to_sync(channel_layer.group_send)(serverName + "Server", to_send)
            server.playerCount = getTicketOutput(ticket)
        else:
            server.playerCount = 0

    return render(request, 'interface/servers.html', {"servers": hasPermissionsTo})

@login_required(login_url = "/login/")
def getOnlineUsers(request, serverName):
    try:
        server = ServerClient.objects.get(name=serverName)
    except:
        return render(request, 'interface/404.html', status=404)

    if server.is_online:
        ticket = createTicket() 
        to_send = {'type':'inquiry', 'inquiry': {'ticket': ticket, 'cmd': 'getOnlinePlayers'}}
        async_to_sync(channel_layer.group_send)(serverName + "Server", to_send)
        players = getTicketOutput(ticket).split(",")
        print(players)
        players_filtered = []
        for p in players:
            p = ''.join(filter(str.isalnum, p)) 
            players_filtered.append(p)
            try:
                pl = NPCPlayer.objects.get(nickname=p)
                if pl.is_currently_online == False:
                    pl.is_currently_online = True
                    pl.was_last_in = serverName
                    pl.last_online = datetime.now()
                    pl.save()
            except:
                pl = NPCPlayer.objects.create(nickname=p)
                if pl.is_currently_online == False:
                    pl.is_currently_online = True
                    pl.was_last_in = serverName
                    pl.last_online = datetime.now()
                    pl.save()

        return render(request, 'interface/playerList.html', {"players": players_filtered, "server": server.name})
    else:
        players_filtered = []
        return render(request, 'interface/playerList.html', {"players": players_filtered, "server": server.name})

@login_required(login_url="/login/")
def playerView(request, playerName):

    notes = Notes.objects.all().filter(player=playerName).order_by('-created_at')
    cnx = mysql.connector.connect(**litebansconfig)
    try:
        player = NPCPlayer.objects.get(nickname=playerName)
    except:
        player = NPCPlayer.objects.create(nickname=playerName)
    cursor = cnx.cursor()
    cursor.execute("SELECT until FROM litebans_bans WHERE uuid='{}' ORDER BY until DESC LIMIT 1".format(player.uuid))
    lastbanwhen = cursor.fetchone()[0]
    cursor2 = cnx.cursor()
    cursor2.execute("SELECT until FROM litebans_mutes WHERE uuid='{}' ORDER BY until DESC LIMIT 1".format(player.uuid))
    lastmutewhen = cursor2.fetchone()[0]
    print(int(time.time()))
    print(lastbanwhen)
    if lastbanwhen > int(time.time() * 1000):
        player.currently_banned = True
    else: 
        player.currently_banned = False

    if lastmutewhen > int(time.time() * 1000):
        player.currently_muted = True
    else: 
        player.currently_muted = False
    cnx.close()
    return render(request, 'interface/player.html', {"player": player, "notes": notes})

@login_required(login_url="/login/")
def addNoteView(request, playerName):
    if request.POST:
        form = AddNoteForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            content = form.cleaned_data.get('body')
            note = Notes.objects.create(player=playerName, madeby=request.user, content=content)
            messages.success(request, f'New note added!')
            return HttpResponseRedirect('/player/'+playerName)

    else:
        form = AddNoteForm()
    
    content = {
        'form': form,
        'playerName': playerName
    }
    return render(request, 'interface/add_note.html', content)

@login_required(login_url="/loign/")
def getLatestNotes(request):
    latestNotes = Notes.objects.all().order_by("-id")[:30]
    content = {
        'notes': latestNotes
    }
    return render(request, 'interface/latest_notes.html', content)


@login_required(login_url="/login/")
def profile(request):
    user = request.user
    profile = Player.objects.get(user=user)
    content = {
        'player': profile,
        'user': user,
    }
    return render(request, 'interface/profile.html', content)


@login_required(login_url="/login/")
def serverLogs(request, serverName):
    user = request.user
    profile = Player.objects.get(user=user)
    try:
        ServerClient.objects.get(name=serverName)
    except:
        return render(request, 'interface/404.html', status=404)
    
    allMessages = ChatMessage.objects.filter(sent_in=serverName).order_by("-sent_on")
    if profile.checkForPermission("administrator") or profile.checkForPermission("readprivmessages"):
        pass
    else:
        for message in allMessages:
            if message.message.startswith("/w ") or message.message.startswith("/msg ") or message.message.startswith("/whisper ") or message.message.startswith("/tell ") or message.message.startswith("/emsg ") or message.message.startswith("/r "):
                message.message = "[***] Censored Command - you need higher permissions."
        
        
    paginator = Paginator(allMessages, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    return render(request, 'interface/chat_log.html', {'page_obj': page_obj, 'subtitle': serverName})

@login_required(login_url="/login/")
def playerLogs(request, playerName):
    try:
        NPCPlayer.objects.get(nickname=playerName)
    except:
        return render(request, 'interface/404.html', status=404)
    
    allMessages = ChatMessage.objects.filter(nickname=playerName).order_by("-sent_on")
    paginator = Paginator(allMessages, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    return render(request, 'interface/chat_log.html', {'page_obj': page_obj, 'subtitle': playerName})



@login_required(login_url="/login/")
def playersPage(request):
    if request.POST:
        search_form = Search(request.POST)
        if search_form.is_valid():

            to_search = search_form.cleaned_data.get('search')
            player_list = []
            for player in NPCPlayer.objects.all().order_by('-last_online'):
                if to_search.lower() in player.nickname.lower():
                    player_list.append(player)

            paginator = Paginator(player_list, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'interface/player_list.html', {'page_obj': page_obj, "form": search_form})

    else:
        player_list = NPCPlayer.objects.all().order_by('-last_online')
        search_form = Search()
        paginator = Paginator(player_list, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        return render(request, 'interface/player_list.html', {'page_obj': page_obj, "form": search_form})