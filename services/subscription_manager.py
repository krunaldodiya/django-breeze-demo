class SubscriptionManager:
    def __init__(self, ws_consumer) -> None:
        self.ws_consumer = ws_consumer

    def subscribe_topic(self, topic):
        return f"subscribed:{topic}"
