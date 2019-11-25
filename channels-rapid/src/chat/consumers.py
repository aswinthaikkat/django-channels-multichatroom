from channels.generic.websocket import WebsocketConsumer
import json
from chat.models import Thread
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("connected")
        other_user = self.scope["url_route"]["kwargs"]["username"]
        current_user = self.scope["user"]
        current_thread = self.get_thread(current_user, other_user)
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)

    def disconnect(self, close_code):
        pass
        print("disconnected")

    def receive(self, text_data):
        print("received", text_data)
        loaded_json = json.loads(text_data)
        print(loaded_json.update({"user": str(self.scope["user"])}))
        async_to_sync(self.channel_layer.group_send)(
            "chat", {"type": "chat_message", "message": json.dumps(loaded_json)}
        )

    def chat_message(self, event):
        print("message", event)
        self.send(text_data=event["message"])

    def get_thread(self, current_user, other_user):
        return Thread.objects.get_or_new(current_user, other_user)[0]

