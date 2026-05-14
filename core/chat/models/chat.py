from django.db import models
from django.contrib.auth.models import User
from common.base_model import BaseModel
from django.utils import timezone


class ChatRoom(BaseModel):
    """Model for chat rooms"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_chat_rooms')
    participants = models.ManyToManyField(
        User, related_name='chat_rooms', through='ChatParticipant')

    class Meta:
        db_table = 'chat_room'
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ChatParticipant(models.Model):
    """Model to track participants in a chat room"""
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='participant_info')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_participations')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'chat_participant'
        unique_together = ('chat_room', 'user')
        verbose_name = 'Chat Participant'
        verbose_name_plural = 'Chat Participants'

    def __str__(self):
        return f"{self.user.get_full_name()} in {self.chat_room.name}"


class ChatMessage(BaseModel):
    """Model for chat messages"""
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()

    class Meta:
        db_table = 'chat_message'
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['chat_room', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"Message from {self.user.get_full_name()} in {self.chat_room.name}"


class ChatActivity(models.Model):
    """Model to track user online/offline status in chat rooms"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='chat_activity')
    is_online = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
    current_room = models.ForeignKey(
        ChatRoom, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='active_users')

    class Meta:
        db_table = 'chat_activity'
        verbose_name = 'Chat Activity'
        verbose_name_plural = 'Chat Activities'

    def __str__(self):
        status = "Online" if self.is_online else "Offline"
        return f"{self.user.get_full_name()} - {status}"

    @classmethod
    def set_user_online(cls, user, room=None):
        """Set user as online"""
        activity, _ = cls.objects.get_or_create(user=user)
        activity.is_online = True
        activity.current_room = room
        activity.last_active = timezone.now()
        activity.save(update_fields=['is_online',
                      'current_room', 'last_active'])
        return activity

    @classmethod
    def set_user_offline(cls, user):
        """Set user as offline"""
        try:
            activity = cls.objects.get(user=user)
            activity.is_online = False
            activity.current_room = None
            activity.last_active = timezone.now()
            activity.save(
                update_fields=['is_online', 'current_room', 'last_active'])
        except cls.DoesNotExist:
            pass
