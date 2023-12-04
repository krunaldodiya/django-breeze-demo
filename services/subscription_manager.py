import os
import threading
import pyotp

from typing import Dict, List
from datetime import datetime

from SmartApi.smartConnect import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2


class SubscriptionManager:
    def __init__(self, ws_consumer) -> None:
        self.ws_consumer = ws_consumer

        self.client_id = os.getenv("CLIENT_ID")

        self.password = os.getenv("PASSWORD")

        self.mpin = os.getenv("MPIN")

        self.api_key = os.getenv("API_KEY")

        self.totp_key = os.getenv("TOTP_KEY")

        self.shutdown_flag = threading.Event()

        self.http_client = self.get_http_client()

        self.ws_clients = {}

        self.room_names: Dict[str, List] = {}

    def get_totp(self, totp_key):
        return pyotp.TOTP(totp_key).now()

    def get_http_client(self):
        return SmartConnect(self.api_key)

    @property
    def ws_client(self):
        try:
            today = datetime.today().strftime("%Y-%m-%d")

            return self.ws_clients[today]
        except KeyError:
            self.ws_clients = {}

            session = self.http_client.generateSession(
                self.client_id,
                self.mpin,
                self.get_totp(self.totp_key),
            )

            ws_client = SmartWebSocketV2(
                session["data"]["jwtToken"],
                self.api_key,
                self.client_id,
                self.http_client.getfeedToken(),
            )

            self.ws_clients[today] = ws_client

            return ws_client

    def start_connection(self):
        threading.Thread(target=self.connect, daemon=True).start()

    def stop_connection(self):
        self.shutdown_flag.set()
        self.room_names[self.ws_consumer.room_name] = []

    def connect(self):
        while not self.shutdown_flag.is_set():
            self.ws_client.on_open = self.on_open
            self.ws_client.on_error = self.on_error
            self.ws_client.on_close = self.on_close
            self.ws_client.on_data = self.on_data

            self.ws_client.connect()
        else:
            self.ws_client.close_connection()

    def on_open(self, wsapp):
        pass

    def on_error(self, wsapp, error):
        pass

    def on_close(self, wsapp):
        pass

    def on_data(self, wsapp, message):
        print(message)

    def get_token_list(self, topic):
        token_data = topic.split("_")

        if len(token_data) != 2:
            return None

        return [{"exchangeType": token_data[0], "tokens": [token_data[1]]}]

    def subscribe(self, topic):
        token_list = self.get_token_list(topic)

        if not token_list:
            return "Invalid Token Data"

        self.ws_client.subscribe("abc123", 2, token_list)

        return True

    def unsubscribe(self, token_list):
        self.ws_client.unsubscribe("abc123", 2, token_list)

    def subscribe_topic(self, topic):
        try:
            topics = self.room_names.setdefault(self.ws_consumer.room_name, [])

            if topic in topics:
                return "already subscribed"

            response = self.subscribe(topic)

            if not response:
                return f"Error subscribing to {topic}"

            topics.append(topic)

            return f"subscribed:{topic}"
        except Exception as e:
            print(e)
