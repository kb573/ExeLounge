from better_profanity import profanity
from bleach.linkifier import Linker
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.html import escape
from six.moves.urllib.parse import urlparse

User = get_user_model


def set_target(attrs, new=False):
    """From https://bleach.readthedocs.io/en/latest/linkify.html#setting-attributes."""

    p = urlparse(attrs[(None, 'href')])
    if p.netloc not in ['my-domain.com', 'other-domain.com']:
        attrs[(None, 'target')] = '_blank'
        attrs[(None, 'class')] = 'external'
    else:
        attrs.pop((None, 'target'), None)
    return attrs


class PublicChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        Called when the websocket is handshaking.
        """
        print("PublicChatConsumer: connect: " + str(self.scope["user"]))
        # let everyone connect. But limit read/write to authenticated users
        await self.accept()

        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            "public_chatroom_1",
            self.channel_name,
        )

    async def disconnect(self, code):
        """
        Called when the WebSocket closes.
        """
        # leave the room
        print("PublicChatConsumer: disconnect")
        pass

    async def receive_json(self, content):
        """
        Called when we get a text frame.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        print("PublicChatConsumer: receive_json: " + str(command))
        print("PublicChatConsumer: receive_json: message: " + str(content["message"]))
        if command == "send":
            if len(content["message"].lstrip()) > 0:
                await self.send_message(content["message"])

    async def send_message(self, message):
        profanity.load_censor_words()
        linker = Linker(callbacks=[set_target])
        await self.channel_layer.group_send(
            "public_chatroom_1",
            {
                "type": "chat.message",
                "full_name": escape(self.scope["user"].get_full_name()),
                "user_id": escape(self.scope["user"].id),
                "message": linker.linkify(profanity.censor(escape(message))),
            }
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        print("PublicChatConsumer: chat_message from user #" + str(event["user_id"]))
        await self.send_json(
            {
                "full_name": event["full_name"],
                "user_id": event["user_id"],
                "message": event["message"],
            },
        )
