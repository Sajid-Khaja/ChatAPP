import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message, UserProfile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Room name based on URL route
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
      data = json.loads(text_data)
      message = data.get("message", "")
      username = data.get("username", "Anonymous")

    # Save the message asynchronously
      await self.save_message(username, message)

    # Get user image asynchronously
      user_image = await self.get_user_image(username)

    # Broadcast message to the group
      await self.channel_layer.group_send(
        self.room_group_name,
        {
            "type": "chat_message",
            "message": message,
            "username": username,
            "user_image": user_image
        }
    )


    async def chat_message(self, event):
        message = event["message"]
        username = event.get("username", "Anonymous")
        user_image = event.get("user_image", "")

        await self.send(text_data=json.dumps({
            "username": username,
            "message": message,
            "user_image": user_image
        }))

    @sync_to_async
    def save_message(self, username, message):
        # Get or create the user (if it does not exist)
        user, created = User.objects.get_or_create(username=username)
        if created:
            # Optionally: Assign a default profile if not present
            UserProfile.objects.get_or_create(user=user)  # Ensure UserProfile is created if not present
        
        # Get or create the room
        room, _ = ChatRoom.objects.get_or_create(name=self.room_name)

        # Save the message
        Message.objects.create(room=room, user=user, content=message)

    @sync_to_async
    def get_user_image(self, username):
        try:
            user = User.objects.get(username=username)
            user_profile = user.profile  # Assuming UserProfile is related via OneToOneField
            return user_profile.image.url if user_profile and user_profile.image else None
        except User.DoesNotExist:
            return None  # Handle case where user does not exist
        except user.profile.RelatedObjectDoesNotExist:
            return None  # Handle case where profile does not exist for user
