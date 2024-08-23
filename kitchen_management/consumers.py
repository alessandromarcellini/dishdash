from channels.generic.websocket import AsyncWebsocketConsumer
import json

class KitchenManagementConsumer(AsyncWebsocketConsumer): #Every time a page connects to the socket a consumer is created. A consumer is related to only one connection.
    async def connect(self): # runs whenever a new user connects to the websocket
        self.kitchen_section_id = self.scope["url_route"]["kwargs"]["kitchen_section_id"]
        self.kitchen_group_name = f"kitchen-{self.kitchen_section_id}"
        await self.channel_layer.group_add(self.kitchen_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code): # runs whenever a user disconnects from the websocket
        self.channel_layer.group_discard(self.kitchen_group_name, self.channel_name)
        print(f"closed with code: {code}")


    async def receive(self, text_data=None, bytes_data=None): #runs every time a user sends data to the websocket
        # THIS IS WHERE THE SERVER RECEIVES A MESSAGE FROM THE CLIENT

        json_data = json.loads(text_data)
        message = json_data["message"]
        sender = json_data["sender"]


        await self.channel_layer.group_send(self.kitchen_group_name, { # SENDS IT TO ALL OTHER CLIENTS
            'type': "kitchen_section_message",
            'message': message,
            'sender': sender,
        })


    # Receive message from room group
    async def kitchen_section_message(self, event):
        # ACTIVATED WHEN CLIENT RECEIVES A MESSAGE WITH THE TYPE OF "kitchen_section_message"
        type = event['type']
        sender = event['sender']
        data = event['data']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': type,
            'sender': sender,
            'data': data
        }))
