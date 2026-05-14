import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']

        # Check authentication
        if not self.user.is_authenticated:
            await self.close()
            return

        # Check participant
        is_participant = await self.check_participant(
            self.room_id,
            self.user.id
        )

        if not is_participant:
            await self.close()
            return

        # Mark user as online
        await self.set_user_online(self.user.id, self.room_id)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Notify user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': self.user.get_full_name() or self.user.username,
                'user_id': self.user.id,
            }
        )

    async def disconnect(self, close_code):

        if hasattr(self, 'room_group_name'):

            # Mark user as offline
            await self.set_user_offline(self.user.id)

            # Notify user left
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'username': self.user.get_full_name() or self.user.username,
                    'user_id': self.user.id,
                }
            )

            # Leave group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data.get('message', '').strip()

        if not message:
            return

        # Save message
        chat_message = await self.save_message(
            self.room_id,
            self.user.id,
            message
        )

        # Trigger async task to send email to offline users
        await self.send_email_notification(chat_message.id)

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.get_full_name() or self.user.username,
                'user_id': self.user.id,
                'timestamp': chat_message.created_at.isoformat(),
            }
        )

    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'timestamp': event['timestamp'],
        }))

    async def user_join(self, event):

        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'message': f"{event['username']} joined the chat",
            'username': event['username'],
            'user_id': event['user_id'],
        }))

    async def user_leave(self, event):

        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'message': f"{event['username']} left the chat",
            'username': event['username'],
            'user_id': event['user_id'],
        }))

    @sync_to_async
    def check_participant(self, room_id, user_id):

        from core.chat.models import ChatParticipant

        return ChatParticipant.objects.filter(
            chat_room_id=room_id,
            user_id=user_id,
            is_active=True
        ).exists()

    @sync_to_async
    def save_message(self, room_id, user_id, message):

        from core.chat.models import ChatMessage

        return ChatMessage.objects.create(
            chat_room_id=room_id,
            user_id=user_id,
            message=message
        )

    @sync_to_async
    def set_user_online(self, user_id, room_id):
        """Mark user as online"""
        from core.chat.models import ChatActivity
        from django.contrib.auth.models import User

        try:
            user = User.objects.get(id=user_id)
            ChatActivity.set_user_online(user, room_id)
        except User.DoesNotExist:
            pass

    @sync_to_async
    def set_user_offline(self, user_id):
        """Mark user as offline"""
        from core.chat.models import ChatActivity
        from django.contrib.auth.models import User

        try:
            user = User.objects.get(id=user_id)
            ChatActivity.set_user_offline(user)
        except User.DoesNotExist:
            pass

    @sync_to_async
    def send_email_notification(self, message_id):
        """Send email notification to offline users"""
        from core.chat.tasks import send_email_to_offline_users

        send_email_to_offline_users.delay(message_id)
