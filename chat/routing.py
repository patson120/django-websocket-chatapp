

from . import consumers
from django.urls import path


websocket_urlpatterns = [
    # path('ws/chat/<str:group>/<str:username>/', consumers.ChatWebSocket.as_asgi()),
    # path('ws/chat/<str:group>/', consumers.ChatWebSocket.as_asgi()),
    path('ws/chat/<str:group>/', consumers.ChatAsyncWebsocketConsumer.as_asgi()),
]
