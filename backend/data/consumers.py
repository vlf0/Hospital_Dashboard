# import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):

    def connect(self):
        async_to_sync(self.channel_layer.group_add('test', self.channel_name))
        self.accept()
        print(self.channel_layer)
        print('accepted')

    def send_notification(self, event):
        self.send(text_data='test_data')
        print('sending')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard('test', self.channel_name))
        print('closed')

