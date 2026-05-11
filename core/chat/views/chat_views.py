from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from core.chat.models import ChatRoom, ChatMessage, ChatParticipant
from django.contrib.auth.models import User


class IsSuperUserMixin(UserPassesTestMixin):
    """Mixin to check if user is superuser"""

    def test_func(self):
        return self.request.user.is_superuser


class ChatListView(LoginRequiredMixin, ListView):
    """List all chat rooms"""
    model = ChatRoom
    template_name = 'chat/chat_list.html'
    context_object_name = 'chat_rooms'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        # Superuser sees all rooms, others see only their rooms
        if user.is_superuser:
            return ChatRoom.objects.all()
        return ChatRoom.objects.filter(participants=user)


class ChatDetailView(LoginRequiredMixin, DetailView):
    """View chat room details with messages"""
    model = ChatRoom
    template_name = 'chat/chat_detail.html'
    context_object_name = 'chat_room'
    pk_url_kwarg = 'room_id'

    def get_queryset(self):
        user = self.request.user
        # Superuser can view any room, others can only view their rooms
        if user.is_superuser:
            return ChatRoom.objects.all()
        return ChatRoom.objects.filter(participants=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_room = self.get_object()
        context['messages'] = ChatMessage.objects.filter(
            chat_room=chat_room
        ).select_related('user').order_by('created_at')
        context['participants'] = ChatParticipant.objects.filter(
            chat_room=chat_room,
            is_active=True
        ).select_related('user')
        # Get list of all users for adding participants (superuser only)
        context['users'] = User.objects.all()
        return context


class ChatCreateView(LoginRequiredMixin, IsSuperUserMixin, CreateView):
    """Create a new chat room (superuser only)"""
    model = ChatRoom
    template_name = 'chat/chat_form.html'
    fields = ['name', 'description', 'is_private']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Add creator as participant
        ChatParticipant.objects.create(
            chat_room=form.instance,
            user=self.request.user
        )
        return response

    def get_success_url(self):
        return reverse_lazy('chat:chat_detail', kwargs={'room_id': self.object.id})


class AddParticipantView(LoginRequiredMixin, IsSuperUserMixin, View):
    """Add participant to chat room (superuser only)"""

    def post(self, request, room_id):
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)

        participant, created = ChatParticipant.objects.get_or_create(
            chat_room=chat_room,
            user=user,
            defaults={'is_active': True}
        )

        if not created:
            participant.is_active = True
            participant.save()

        return redirect('chat:chat_detail', room_id=room_id)


class RemoveParticipantView(LoginRequiredMixin, IsSuperUserMixin, View):
    """Remove participant from chat room (superuser only)"""

    def post(self, request, room_id):
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        user_id = request.POST.get('user_id')

        ChatParticipant.objects.filter(
            chat_room=chat_room,
            user_id=user_id
        ).update(is_active=False)

        return redirect('chat:chat_detail', room_id=room_id)


class DashboardView(LoginRequiredMixin, View):
    """Dashboard view with role-based access"""

    def get(self, request):
        user = request.user

        # Non-superuser redirects to chat
        if not user.is_superuser:
            # Get user's first chat room or redirect to chat list
            chat_rooms = ChatRoom.objects.filter(participants=user)
            if chat_rooms.exists():
                return redirect('chat:chat_detail', room_id=chat_rooms.first().id)
            return redirect('chat:chat_list')

        # Superuser sees full dashboard
        return redirect('employees:dashboard')
