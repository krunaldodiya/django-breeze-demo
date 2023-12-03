import json

from urllib.parse import parse_qs

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

from services.subscription_manager import SubscriptionManager


class WebsocketConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.room_id = None

        self.subscription_manager = SubscriptionManager(self)

    def get_room_id(self):
        query_string = self.scope["query_string"].decode("utf-8")
        query_params = parse_qs(query_string)
        room_id = query_params.get("room_id", [None])[0]

        return f"ticker.{room_id}"

    def connect(self):
        self.room_id = self.get_room_id()

        async_to_sync(self.channel_layer.group_add)(self.room_id, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_id, self.channel_name)

    def receive(self, text_data):
        if text_data.startswith("subscribe:"):
            topics = text_data.split(":")[1].split(",")

            for topic in topics:
                response = self.subscription_manager.subscribe_topic(topic)

                async_to_sync(self.channel_layer.group_send)(
                    self.room_id, {"type": "send_message", "message": response}
                )

    def send_message(self, event):
        self.send(text_data=json.dumps(event["message"]))
