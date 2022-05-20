import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from blackjack.settings import REDIS_HOST, REDIS_PORT
from . import views

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        redis_tables_db = redis.Redis(
         host= REDIS_HOST,
         port= REDIS_PORT,
         db = 1
        )
        self.room_name = 'medium' #  self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'table_%s' % self.room_name
        
        table_list = redis_tables_db.keys()
        ingame_list = []
        print(table_list)
        for table in table_list:
            ingame_list.extend(redis_tables_db.lrange(table, 0, -1))

        for i in range(len(ingame_list)):
            ingame_list[i] = int(ingame_list[i].decode())
        
        
        if not redis_tables_db.exists(self.room_name) and self.scope['user'].id not in ingame_list:
            redis_tables_db.lpush(self.room_name, self.scope['user'].id)
        # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        if redis_tables_db.llen(self.room_name) < 7 and self.scope['user'].id not in ingame_list:
            redis_tables_db.lpush(self.room_name, self.scope['user'].id)
        else:
            await self.close(4004)


    async def disconnect(self, close_code):
        redis_db = redis.Redis(
         host= REDIS_HOST,
         port= REDIS_PORT,
         db = 1
        )


        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
        )
        if close_code != 4004:
            redis_db.lrem(self.room_name, 1, self.scope['user'].id)
        


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        print(event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))