import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BattleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'battle_{self.room_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Notify others of new connection
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'battle_message',
                'message': {
                    'event': 'user_connected',
                    'user': self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
                }
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Parse the incoming JSON
        data = json.loads(text_data)
        
        # Forward message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'battle_message',
                'message': data
            }
        )

    # Send message to WebSocket
    async def battle_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))