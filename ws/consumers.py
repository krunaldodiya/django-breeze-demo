import json

from urllib.parse import parse_qs

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

from services.subscription_manager import SubscriptionManager


class WebsocketConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.subscription_manager = SubscriptionManager()

    def get_room_name(self):
        query_string = self.scope["query_string"].decode("utf-8")
        query_params = parse_qs(query_string)
        room_id = query_params.get("room_id", [None])[0]

        if not room_id:
            raise Exception("room_id is required")

        return f"ticker.{room_id}"

    def connect(self):
        self.room_name = self.get_room_name()

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

        self.close()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "send_message", "message": message}
        )

    def send_message(self, event):
        self.send(text_data=json.dumps(event))
