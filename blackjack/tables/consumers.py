import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from . import views

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        redis_db = redis.Redis(
		 host= '192.168.179.33',
		 port= '6379',
		 db = 1
		)
        conn_list = redis_db.lrange("connections", 0, -1)
        for i in range(len(conn_list)):
            conn_list[i] = int(conn_list[i].decode("utf-8"))
        if redis_db.llen("connections") < 7 and self.scope['user'].id not in conn_list:
            redis_db.lpush("connections", self.scope['user'].id)

            print(self.scope['user'])
            self.room_name = 'medium'
            self.room_group_name = 'table_%s' % self.room_name
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.accept()
            await self.disconnect(404)

    async def disconnect(self, close_code):
        redis_db = redis.Redis(
		 host= '192.168.179.33',
		 port= '6379',
		 db = 1
		)
        conn_list = redis_db.lrange("connections", 0, -1)
        for i in range(len(conn_list)):
            conn_list[i] = int(conn_list[i].decode("utf-8"))

        if self.scope['user'].id in conn_list:
            await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            )
            redis_db.lrem("connections", 1, self.scope['user'].id)
        


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