from django.urls import path
from core.chat.views import (
    ChatListView,
    ChatDetailView,
    ChatCreateView,
    AddParticipantView,
    RemoveParticipantView,
    DashboardView,
)

app_name = 'chat'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('list/', ChatListView.as_view(), name='chat_list'),
    path('create/', ChatCreateView.as_view(), name='chat_create'),
    path('<int:room_id>/', ChatDetailView.as_view(), name='chat_detail'),
    path('<int:room_id>/add-participant/',
         AddParticipantView.as_view(), name='add_participant'),
    path('<int:room_id>/remove-participant/',
         RemoveParticipantView.as_view(), name='remove_participant'),
]
