from django.db import models
from django.contrib.auth.models import User
from common.base_model import BaseModel


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
