from django.urls import re_path

from . import consumers

websocket_urlpatterns = [    
    re_path(r'ws/client/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'ws/server/chat/(?P<token>\w+)/$', consumers.ServerConsumer.as_asgi()),
    # url(r'^ws/client/chat/(?P<token>[^/]+)/$', consumers.ServerConsumer.as_asgi()),
    re_path(r'ws/server/chat/(?P<token>[0-9a-f-]+)/$', consumers.ServerConsumer.as_asgi()),
]
