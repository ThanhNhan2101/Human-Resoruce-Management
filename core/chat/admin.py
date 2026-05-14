from django.contrib import admin
from core.chat.models import ChatRoom, ChatMessage, ChatParticipant, ChatActivity


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'is_private', 'created_at']
    list_filter = ['is_private', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'chat_room', 'created_at']
    list_filter = ['chat_room', 'created_at']
    search_fields = ['message', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChatParticipant)
class ChatParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'chat_room', 'joined_at', 'is_active']
    list_filter = ['is_active', 'joined_at']
    search_fields = ['user__username', 'chat_room__name']


@admin.register(ChatActivity)
class ChatActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_online', 'current_room', 'last_active']
    list_filter = ['is_online', 'last_active']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_active']

    def get_readonly_fields(self, request, obj=None):
        """Make last_active always readonly"""
        return list(self.readonly_fields) + ['user']
