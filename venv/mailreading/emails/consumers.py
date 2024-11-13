import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from ast import literal_eval
from .parser import parse_message,get_from_email
import re
from .models import Email, File


class MessagesConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = literal_eval(text_data)
        self.group_name = re.sub('[^a-zA-Z0-9_.-]', '_', text_data['login'])

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        parse_message(text_data['mail_pass'], text_data['login'], text_data['mail_name'])

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            'messages',
            self.channel_name
        )

    async def send_messages(self, event):
        message = event['message']
        dct=await get_from_email(message)
        await asyncio.sleep(1)

        await self.send(json.dumps(dct))
        await asyncio.sleep(1)
