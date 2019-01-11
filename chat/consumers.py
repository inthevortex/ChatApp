# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import urllib.parse
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'lobby'
        self.room_group_name = 'chat_%s' % self.room_name
        params = urllib.parse.parse_qs(self.scope['query_string'])
        print(params)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': username + ': ' + message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        print('event')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))