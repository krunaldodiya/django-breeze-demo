import json

from urllib.parse import parse_qs

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer


class WebsocketConsumer(WebsocketConsumer):
    @property
    def room_name(self):
        query_string = self.scope["query_string"].decode("utf-8")
        query_params = parse_qs(query_string)
        room_id = query_params.get("room_id", [None])[0]

        return f"ticker.{room_id}"

    def connect(self):
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
        print("event", event)
        # self.send(text_data=json.dumps(event))
