import json
from channels.generic.websocket import WebsocketConsumer
from .models import ServerClient
import uuid
import redis
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer


r = redis.Redis(host='localhost', port=6380, db=0)
channel_layer = get_channel_layer()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = room_name
        print(self.room_group_name)
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name)


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def message(self, event):
        print(event)
        self.send(text_data=json.dumps(event))


class ServerConsumer(WebsocketConsumer):
    def connect(self):
        token = self.scope['url_route']['kwargs']['token']
        print(token)
        try:
            sc = ServerClient.objects.get(token=uuid.UUID(token))
            self.ServerName = sc.name
            print(self.ServerName)
        except:
            self.close()
            return

        print("Accepted Server with ID: " + str(sc.id))

    

        self.accept()

    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data_json)
        print(message)
        # message = text_data_json['message']

        # self.send(text_data=json.dumps({
        #     'message': text_data_json
        # }))
        async_to_sync(self.channel_layer.group_send)(
            self.ServerName, {"type":"message", "message": message}
        )

        # await self.channel_layer.send_json(self.ServerName, text_data_json)