from os import access
from interface.serverFunctions.getPlayers import getPlayerCount
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import ChatMessage, NPCPlayer, Report, ServerClient, Player, Notes
import uuid
import redis
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from .serverFunctions.getPlayers import getPlayerCount
from .supportFunctions.tickets import *
from django.core.paginator import Paginator

from datetime import date, datetime

r = redis.Redis(host='localhost', port=6380, db=0)
channel_layer = get_channel_layer()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        try:
            self.user = User.objects.get(username=self.user)
            self.profile = Player.objects.get(user=self.user)
            print(self.profile.minecraftUsername)
        except:
            self.close()
            return
        print(self.user)
        room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = room_name 
        print(self.room_group_name)
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name)



    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message'] 
        authorUUID = str(self.profile.uuid)
        objWS = {"authorUUID": authorUUID, "text": message}
        obj = {"author": self.profile.minecraftUsername, "text": message}

        print(obj)
        
        self.send(text_data=json.dumps({
            'message': obj
        }))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name + "Server", {"type":"message", "message": objWS} # replace Survival with 
        )

        ChatMessage.objects.create(nickname=self.profile.minecraftUsername, message=message, sent_on=datetime.now(), sent_in=self.room_group_name)

        # objWS = {"authorUUID": "dqweqe", "text": "yes"}
        # async_to_sync(channel_layer.group_send)(
        #         "SurvivalServer", {"type":"message", "message": objWS} # replace Survival with 
        #     )
        print("sent")
        # response = getTicketOutput(ticket)
        # print(response)

    def message(self, event):
        if self.profile.checkForPermission("administrator") or self.profile.checkForPermission("readprivmessages"):
            pass
        else:
            msg = event["message"]["text"]
            if msg.startswith("/w ") or msg.startswith("/msg ") or msg.startswith("/whisper ") or msg.startswith("/tell ") or msg.startswith("/emsg ") or msg.startswith("/r "):
                event["message"]["text"] = "[***] Censored Command - you need higher permissions."
        self.send(text_data=json.dumps(event))


# class ServerConsumer(WebsocketConsumer):
#     def connect(self):
#         token = self.scope['url_route']['kwargs']['token']
#         print(token)
#         try:
#             sc = ServerClient.objects.get(token=uuid.UUID(token))
#             self.ServerName = sc.name
#             sc.is_online = True
#             sc.save()
#             self.sc = sc
#             print(sc.is_online)
#             print(self.ServerName)
#         except:
#             self.close()
#             return

#         # should enumerate Servers and stuff and where the user has righs

#         async_to_sync(self.channel_layer.group_add)(
#             # self.ServerName + "Server", self.channel_name)
#             "SurvivalServer", self.channel_name)


#         print("Accepted Server with ID: " + str(sc.id))
    

#         self.accept()

#     def disconnect(self, close_code):
#         sc = self.sc
#         sc.is_online = False
#         sc.save()
#         async_to_sync(self.channel_layer.group_discard)(
#             self.ServerName + "Server", self.channel_name)
#         print(sc.is_online)

        


#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         print(text_data_json)
#         if "inquiryResponse" in text_data_json:
#             text_data_json = text_data_json["inquiryResponse"]
#             ticket = text_data_json["ticket"]
#             response = text_data_json["response"]
#             if r.get(ticket) == b'reserved':
#                 r.set(ticket, json.dumps(response))
#         else:
#             message = text_data_json['message']
#             print(message)
#             # message = text_data_json['message']

#             # self.send(text_data=json.dumps({
#             #     'message': text_data_json
#             # }))
#             async_to_sync(self.channel_layer.group_send)(
#                 self.ServerName, {"type":"message", "message": message}
#             )

#     def message(self, event):
#         print(event)
#         print(event["message"])
#         print("77")
#         self.send(text_data=json.dumps({"message": event["message"]}))

#     def inquiry(self, event):
#         print(event)
#         self.send(text_data=json.dumps({"inquiry": event["inquiry"]}))

class ClientCousumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        try:
            self.user = User.objects.get(username=self.user)
            self.profile = Player.objects.get(user=self.user)
        except:
            self.close()
            return
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.user.username, self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user.username, self.channel_name)

    def playerCount(self, event):
        print(event)
        self.send(text_data=json.dumps({"inquiry": event["inquiry"]}))


class ServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope['url_route']['kwargs']['token']
        print(token)
        try:
            sc = ServerClient.objects.get(token=uuid.UUID(token))
            self.ServerName = sc.name
            sc.is_online = True
            sc.save()
            self.sc = sc
            print(sc.is_online)
            print(self.ServerName)
        except:
            await self.close()
            return

        # should enumerate Servers and stuff and where the user has righs

        await self.channel_layer.group_add(
            # self.ServerName + "Server", self.channel_name)
            sc.name + "Server", self.channel_name)


        print("Accepted Server with ID: " + str(sc.id))
        await self.accept()

        # ticket = createTicket() 
        # to_send = {'type':'inquiry', 'inquiry': {'ticket': ticket, 'cmd': 'getOnlinePlayers'}}
        # await self.send(text_data=json.dumps(to_send))
        # players = getTicketOutput(ticket).split(",")
        # print(players)
        # players_filtered = []
        # for p in players:
        #     p = ''.join(filter(str.isalnum, p)) 
        #     players_filtered.append(p)
        #     try:
        #         pl = NPCPlayer.objects.get(nickname=p)
        #         if pl.is_currently_online == False:
        #             pl.is_currently_online = True
        #             pl.was_last_in = self.ServerName
        #             pl.last_online = datetime.now()
        #             pl.save()
        #     except:
        #         pl = NPCPlayer.objects.create(nickname=p)
        #         if pl.is_currently_online == False:
        #             pl.is_currently_online = True
        #             pl.was_last_in = self.ServerName
        #             pl.last_online = datetime.now()
        #             pl.save()



    async def disconnect(self, close_code):
        sc = self.sc
        sc.is_online = False
        sc.save()
        await self.channel_layer.group_discard(
            self.ServerName + "Server", self.channel_name)
        print(sc.is_online)
        players = NPCPlayer.objects.filter(was_last_in=self.ServerName)
        for player in players:
            player.is_currently_online = False
            player.last_online = datetime.now()
            player.save()
        


        


    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except:
            return
        print(text_data_json)
        redis = await aioredis.create_redis(
        'redis://localhost:6380')
        if "inquiryResponse" in text_data_json:
            text_data_json = text_data_json["inquiryResponse"]
            ticket = text_data_json["ticket"]
            response = text_data_json["response"]
            if await redis.get(ticket) == b'reserved':
                await redis.set(ticket, json.dumps(response))
        elif "message" in text_data_json:
            message = text_data_json['message']
            print(message)
            # message = text_data_json['message']

            # self.send(text_data=json.dumps({
            #     'message': text_data_json
            # }))
            await self.channel_layer.group_send(
                self.ServerName, {"type":"message", "message": message}
            )
            ChatMessage.objects.create(nickname=message["author"], message=message["text"], sent_on=datetime.now(), sent_in=self.ServerName)
        elif "noteContent" in text_data_json:
            text_data_json = text_data_json["noteContent"]
            note = text_data_json["note"]
            userUsername = text_data_json["username"]
            madebyUUID = text_data_json["madebyUUID"]
            try:
                madebyPlayer = Player.objects.get(uuid=uuid.UUID(madebyUUID))
            except:
                print("[***] Player with UUID {} has no account in the interface!".format(madebyUUID))
            madebyUser = madebyPlayer.user
            print(madebyUser)
            Notes.objects.create(player=userUsername, madeby=madebyUser, content=note)

        elif "getNoteRequest" in text_data_json:
            text_data_json = text_data_json["getNoteRequest"]
            username = text_data_json["username"]
            requestedByUUID = text_data_json["requestedByUUID"]
            page_number = text_data_json["page"]
            if page_number < 1:
                page_number = 1
            print(text_data_json)
            print(requestedByUUID)
            notes = Notes.objects.all().filter(player=username).order_by("-created_at")
            notesToSendBack = {}
            notesToSendBack["requesterUUID"] = requestedByUUID
            allNotes = []
            paginator = Paginator(notes, 3)
            page_obj = paginator.get_page(page_number)
            print(page_obj)
            for note in page_obj:
                oneNote = {
                    "id": note.id,
                    "madeBy": User.objects.get(id=note.madeby_id).username,
                    "content": note.content
                }
                allNotes.append(oneNote)

            notesToSendBack["notes"] = allNotes
            print(notesToSendBack)
            # await self.channel_layer.group_send(self.ServerName+"Server", allNotes)
            await self.send(text_data=json.dumps({"notesResponse": notesToSendBack}))
            print(notes)
        elif "playerStatusChanged" in text_data_json:
            text_data_json = text_data_json["playerStatusChanged"]
            nickname = text_data_json["playerNickname"]
            isOnline = text_data_json["isOnline"]
            try:
                player = NPCPlayer.objects.get(nickname=nickname)
            except:
                player = NPCPlayer.objects.create(nickname=nickname, last_online=datetime.now())
            print(player)
            print(isOnline)
            player.is_currently_online = isOnline
            player.was_last_in = self.ServerName
            player.last_online = datetime.now()
            if player.uuid == None:
                player.uuid = text_data_json["uuid"]
            player.save()
        elif "reportContent" in text_data_json:
            text_data_json = text_data_json["reportContent"]
            made_by = text_data_json["made_by"]
            content = text_data_json["content"]
            target = text_data_json["target"]
            madeByPlayer = NPCPlayer.objects.get(nickname=made_by)
            if madeByPlayer.is_allowed_to_report:
                report = Report.objects.create(made_by = made_by, content=content, made_in = self.ServerName, target=target)
                print(report)
            else:
                pass
        elif "reportAbilityChange" in text_data_json:
            text_data_json = text_data_json["reportAbilityChange"]
            player = text_data_json["player"]
            alloworNot = text_data_json["allow"]
            try:
                player = NPCPlayer.objects.get(nickname=player)
                player.is_allowed_to_report = alloworNot
                player.save()
            except:
                pass

    async def message(self, event):
        print(event)
        print(event["message"])
        print("77")
        await self.send(text_data=json.dumps({"message": event["message"]}))


    async def inquiry(self, event):
        print(event)
        await self.send(text_data=json.dumps({"inquiry": event["inquiry"]}))
