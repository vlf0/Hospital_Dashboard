import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):

    groups = ['plan']

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add('plan', self.channel_name))

    def send_notification(self, event):
        message = json.dumps(event['message'])
        self.send(text_data=message)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard('plan', self.channel_name))


