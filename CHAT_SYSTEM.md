# Chat System - Tóm Tắt Triển Khai

## Mô Tả Tính Năng

Hệ thống chat real-time cho phép nhân viên giao tiếp trong các phòng chat. Khi người dùng offline, họ sẽ nhận được email thông báo tin nhắn mới. Hệ thống theo dõi trạng thái online/offline của người dùng và hỗ trợ quản lý phòng chat và thành viên tham gia.

**Công nghệ sử dụng**: Django Channels + WebSocket + Redis + Celery + PostgreSQL

## Các Thay Đổi Được Thực Hiện

### 1. **Dependencies** (`requirements.txt`)

Các packages được sử dụng:

```
channels==4.0.0
daphne==4.0.0
channels-redis==4.1.0
celery==5.3.4
django-celery-beat==2.5.0
redis==5.0.1
```

**Giải thích**:

- `channels`: WebSocket support cho Django
- `daphne`: ASGI server để chạy Channels
- `channels-redis`: Redis backend cho Channels layer
- `celery` + `django-celery-beat`: Task queue cho gửi email async
- `redis`: In-memory message broker cho Celery

### 2. **Channels Configuration** (`config/asgi.py`)

File ASGI configuration cho phép kết nối WebSocket:

```python
from core.chat.routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
```

**Giải thích**:

- `ProtocolTypeRouter`: Phân loại request theo protocol (HTTP hoặc WebSocket)
- `AuthMiddlewareStack`: Xác thực người dùng cho WebSocket
- `AllowedHostsOriginValidator`: Bảo mật WebSocket (chỉ cho phép hosts được cấu hình)

### 3. **Django Settings** (`config/settings/base.py`)

#### Channels Configuration:

```python
ASGI_APPLICATION = 'config.asgi.application'

REDIS_HOST = env('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = env.int('REDIS_PORT', default=6379)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
        },
    },
}
```

#### Installed Apps:

```python
INSTALLED_APPS = [
    'channels',  # Must be first for Channels
    'core.chat',
    # ...
]
```

### 4. **Chat Routing** (`core/chat/routing.py`)

```python
from django.urls import re_path
from core.chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', ChatConsumer.as_asgi()),
]
```

Định nghĩa URL pattern cho WebSocket connections.

### 5. **Chat Consumer** (`core/chat/consumers.py`)

AsyncWebsocketConsumer xử lý các kết nối WebSocket:

**Main Methods**:

- `connect()`:
  - Lấy `room_id` từ URL
  - Kiểm tra authentication và participant status
  - Đánh dấu user online
  - Thêm user vào group broadcast
  - Gửi thông báo user joined

- `disconnect()`:
  - Đánh dấu user offline
  - Gửi thông báo user left
  - Rời khỏi group broadcast

- `receive()`:
  - Nhận message từ client
  - Validate message
  - Lưu vào database
  - Broadcast message tới group
  - Trigger email task cho offline users

- `user_join()` / `user_leave()` / `chat_message()`:
  - Các handler cho broadcast events

### 6. **Chat Models** (`core/chat/models/chat.py`)

#### **ChatRoom**

```python
class ChatRoom(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        User, related_name='chat_rooms', through='ChatParticipant'
    )
```

#### **ChatParticipant**

```python
class ChatParticipant(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('chat_room', 'user')
```

Quản lý trạng thái tham gia của người dùng trong phòng chat.

#### **ChatMessage**

```python
class ChatMessage(BaseModel):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['chat_room', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
```

Lưu trữ tin nhắn với indexes để tối ưu hóa truy vấn.

#### **ChatActivity**

```python
class ChatActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
    current_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)
```

Theo dõi trạng thái online/offline và phòng hiện tại của user.

**Methods**:

- `set_user_online(user, room)`: Đánh dấu user online
- `set_user_offline(user)`: Đánh dấu user offline

### 7. **Chat Usecase Layer** (`core/chat/usecase/`)

#### Selectors (`selectors/`):

- Các hàm truy vấn dữ liệu (read-only)
- Ví dụ: `get_chat_rooms()`, `get_messages()`, `get_participants()`

#### Services (`services/`):

- Các hàm thực hiện business logic
- Ví dụ: `create_chat_room()`, `add_participant()`, `send_message()`

### 8. **Chat Tasks** (`core/chat/tasks.py`)

#### **Task 1: `send_email_to_offline_users`**

Được trigger khi có message mới:

```python
@shared_task(bind=True, max_retries=3)
def send_email_to_offline_users(self, message_id):
```

**Logic**:

1. Lấy message từ DB
2. Tìm tất cả participants trong room
3. Kiểm tra ai đang offline (`ChatActivity.is_online = False`)
4. Gửi email notification cho offline users
5. Retry tối đa 3 lần nếu lỗi (exponential backoff 5 seconds)

**Email Template**: `templates/email/new_message_notification.html`

#### **Task 2: `cleanup_offline_status`** (Periodic)

Định kỳ reset status online cho những user inactive > 30 phút:

```python
@shared_task
def cleanup_offline_status():
    threshold_time = timezone.now() - timedelta(minutes=30)
    offline_count = ChatActivity.objects.filter(
        is_online=True,
        last_active__lt=threshold_time
    ).update(is_online=False, current_room=None)
```

### 9. **Chat Views** (`core/chat/views/chat_views.py`)

#### **ChatListView** (ListView)

- Hiển thị danh sách phòng chat
- Superuser: thấy tất cả rooms
- User thường: chỉ thấy rooms của họ

#### **ChatDetailView** (DetailView)

- Hiển thị chi tiết phòng chat
- Danh sách messages, participants
- WebSocket endpoint để chat real-time

#### **ChatCreateView** (CreateView)

- Tạo phòng chat mới (superuser only)
- Auto-add creator as participant

#### **AddParticipantView**

- Thêm người dùng vào phòng chat

#### **RemoveParticipantView**

- Xóa người dùng khỏi phòng chat

#### **DashboardView**

- Dashboard tổng quan chat

### 10. **Chat URLs** (`core/chat/urls.py`)

```python
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('list/', ChatListView.as_view(), name='chat_list'),
    path('create/', ChatCreateView.as_view(), name='chat_create'),
    path('<int:room_id>/', ChatDetailView.as_view(), name='chat_detail'),
    path('<int:room_id>/add-participant/', AddParticipantView.as_view(), name='add_participant'),
    path('<int:room_id>/remove-participant/', RemoveParticipantView.as_view(), name='remove_participant'),
]
```

### 11. **Chat Admin** (`core/chat/admin.py`)

- `ChatRoomAdmin`: Quản lý phòng chat
- `ChatParticipantAdmin`: Quản lý thành viên
- `ChatMessageAdmin`: Xem messages
- `ChatActivityAdmin`: Theo dõi trạng thái online/offline

### 12. **Templates** (`templates/chat/`)

- `chat_list.html`: Danh sách phòng chat
- `chat_detail.html`: Chi tiết phòng chat + WebSocket client
- `chat_form.html`: Form tạo phòng chat

## Workflow - Luồng Hoạt Động

### 1. **Tạo Phòng Chat**

```
User (Superuser) → ChatCreateView → Create ChatRoom + ChatParticipant
```

### 2. **Kết Nối WebSocket**

```
Client (Browser)
  → WebSocket Connect (ws://host/ws/chat/room_id/)
  → ChatConsumer.connect()
  → Check authentication & participant
  → ChatActivity.set_user_online()
  → group_add(chat_group)
  → Send user_join broadcast
```

### 3. **Gửi Message**

```
Client → ChatConsumer.receive()
  → Validate message
  → Save to ChatMessage
  → Trigger send_email_to_offline_users task
  → group_send(chat_message) to all clients
  → Clients nhận message & update UI
```

### 4. **Gửi Email (Offline)**

```
send_email_to_offline_users task (Celery)
  → Get ChatMessage
  → Find offline participants
  → Render email template
  → send_mail() to offline users
```

### 5. **Ngắt Kết Nối WebSocket**

```
Client → ChatConsumer.disconnect()
  → ChatActivity.set_user_offline()
  → group_discard()
  → Send user_leave broadcast
```

## Frontend WebSocket Integration

### Client-side Connection

```javascript
// templates/chat/chat_detail.html

const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomId + "/",
);

chatSocket.onopen = function () {
  console.log("Connected to chat room");
};

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  // Handle different message types:
  // - 'chat_message': new message
  // - 'user_join': user joined
  // - 'user_leave': user left
  updateChatUI(data);
};
```

### Sending Message

```javascript
document.getElementById("sendBtn").addEventListener("click", function () {
  const message = document.getElementById("messageInput").value;
  chatSocket.send(
    JSON.stringify({
      message: message,
    }),
  );
  document.getElementById("messageInput").value = "";
});
```

## Database Tables

```
chat_room                  - Phòng chat
chat_participant           - Thành viên tham gia
chat_message               - Tin nhắn
chat_activity              - Trạng thái online/offline
```

## Configuration Environment Variables

```env
# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# Email (cho email notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@hrm.com
```

## Docker Setup

```yaml
# docker-compose.yml

services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"

  web:
    build: .
    command: daphne -b 0.0.0.0 -p 8000 config.asgi:application
    depends_on:
      - redis
      - db
```

**Chạy Daphne ASGI server thay vì Gunicorn để support WebSocket**.

## Chạy Hệ Thống Locally

### 1. Setup venv & dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Migrate database

```bash
python manage.py migrate
```

### 3. Seed data

```bash
python manage.py seed_data
```

### 4. Chạy development server (Daphne)

```bash
# Option 1: Daphne (chỉ ASGI)
daphne -b 0.0.0.0 -p 8000 config.asgi:application

# Option 2: Daphne + Celery worker
daphne -b 0.0.0.0 -p 8000 config.asgi:application &
celery -A config worker -l info
```

### 5. Chạy Redis (nếu locally)

```bash
redis-server
# hoặc dùng Docker
docker run -p 6379:6379 redis:7
```

## Files Liên Quan

```
core/chat/
├── admin.py                    - Django admin
├── apps.py                     - App config
├── consumers.py                - WebSocket consumer
├── routing.py                  - WebSocket URL routing
├── tasks.py                    - Celery tasks
├── urls.py                     - HTTP URLs
├── models/
│   └── chat.py                - ChatRoom, ChatMessage, ChatActivity, ChatParticipant
├── usecase/
│   ├── selectors/             - Read queries
│   └── services/              - Business logic
└── views/
    └── chat_views.py          - Views

config/
├── asgi.py                     - ASGI config (Channels setup)
├── settings/
│   └── base.py                - Channels config
└── celery.py                  - Celery config

templates/
├── chat/
│   ├── chat_list.html         - List rooms
│   ├── chat_detail.html       - Chat interface + WebSocket
│   └── chat_form.html         - Create room
└── email/
    └── new_message_notification.html  - Email template
```

## Key Features

✅ Real-time messaging dengan WebSocket
✅ Online/Offline status tracking
✅ Email notification cho offline users
✅ Room-based chat (multiple participants)
✅ Message history & persistence
✅ Superuser management console
✅ Participant management (add/remove)
✅ Scalable với Redis channel layer
✅ Async task processing với Celery

## Potential Improvements

- [ ] Message encryption
- [ ] File sharing support
- [ ] Typing indicators
- [ ] Message reactions/emojis
- [ ] Message search
- [ ] Chat room archiving
- [ ] Read receipts
- [ ] Message editing/deletion
- [ ] Rate limiting
- [ ] Analytics & metrics

## Troubleshooting

**Issue**: WebSocket connection refused

- Kiểm tra Redis đang chạy: `redis-cli ping`
- Kiểm tra Daphne chạy thay vì Gunicorn
- Kiểm tra ASGI_APPLICATION setting

**Issue**: Email không được gửi

- Kiểm tra Celery worker chạy
- Kiểm tra Redis connection
- Kiểm tra EMAIL settings

**Issue**: Messages không broadcast

- Kiểm tra CHANNEL_LAYERS config
- Kiểm tra Redis host/port
- Restart Daphne & Redis
