from ..supportFunctions.tickets import createTicket, deleteTicket, getTicketOutput
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
import time 
channel_layer = get_channel_layer()
import threading
import asyncio

def getPlayerCount(ticket, serverName):
    print(ticket)
    print(channel_layer)
    print(serverName)
    to_send = {'type':'inquiry', 'inquiry': {'ticket': ticket, 'cmd': 'getOnlinePlayerCount'}}
    async_to_sync(channel_layer.group_send)(serverName + "Server", to_send)
    