import json

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

from services.subscription_manager import SubscriptionManager


class WebsocketConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None

        self.room_name = None

        self.subscription_manager = SubscriptionManager(self)

    def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            self.close(code=401)
        else:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

            async_to_sync(self.channel_layer.group_add)(
                self.room_name, self.channel_name
            )

            self.subscription_manager.start_connection()

            self.accept()

    def disconnect(self, close_code):
        if self.room_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_name, self.channel_name
            )

            self.subscription_manager.stop_connection()

    def receive(self, text_data):
        if text_data.startswith("subscribe:"):
            topics = text_data.split(":")[1].split(",")

            for topic in topics:
                response = self.subscription_manager.subscribe_topic(topic)

                async_to_sync(self.channel_layer.group_send)(
                    self.room_name, {"type": "send_message", "message": response}
                )

    def send_message(self, event):
        self.send(text_data=json.dumps(event["message"]))
