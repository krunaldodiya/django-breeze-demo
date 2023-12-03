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

        self.client = self.get_client()

        self.ws_clients = {}

        self.room_ids: Dict[str, List] = {}

    @property
    def sws(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")

            return self.ws_clients[today]
        except KeyError:
            self.ws_clients = {}

            feed_token = self.client.getfeedToken()

            data = self.client.generateSession(
                self.client_id,
                self.mpin,
                self.get_totp(self.totp_key),
            )

            auth_token = data["data"]["jwtToken"]

            sws = SmartWebSocketV2(
                auth_token,
                self.api_key,
                self.client_id,
                feed_token,
            )

            self.ws_clients[today] = sws

            return sws

    def get_totp(self, totp_key):
        return pyotp.TOTP(totp_key).now()

    def get_client(self):
        return SmartConnect(self.api_key)

    def get_token_list(self, topic):
        token_data = topic.split("_")

        if len(token_data) != 2:
            return None

        return [{"exchangeType": token_data[0], "tokens": [token_data[1]]}]

    def subscribe(self, topic):
        token_list = self.get_token_list(topic)

        if not token_list:
            return "Invalid Token Data"

        self.sws.subscribe("abc123", 2, token_list)

        return True

    def unsubscribe(self, token_list):
        self.sws.unsubscribe("abc123", 2, token_list)

    def subscribe_topic(self, topic):
        topics = self.room_ids.setdefault(self.ws_consumer.room_id, [])

        if topic in topics:
            return "already subscribed"

        response = self.subscribe(topic)

        if not response:
            return f"Error subscribing to {topic}"

        topics.append(topic)

        return f"subscribed:{topic}"
