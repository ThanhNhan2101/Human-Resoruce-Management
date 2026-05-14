# Celery Email Notification - Tóm Tắt Triển Khai

## Mô Tả Tính Năng

Hệ thống gửi email thông báo cho những user offline khi có tin nhắn mới trong chat room. Nếu user đang online (kết nối WebSocket), sẽ không gửi email.

**Công nghệ sử dụng**: Celery + Redis + Django Email Backend

## Các Thay Đổi Được Thực Hiện

### 1. **Dependencies** (`requirements.txt`)

Thêm packages:

```
celery==5.3.4
django-celery-beat==2.5.0
redis==5.0.1
```

### 2. **Celery Configuration** (`config/celery.py`)

- Tạo file cấu hình Celery
- Cấu hình broker (Redis) và result backend
- Autodiscover tasks từ tất cả app
- JSON serialization cho messages

### 3. **Django Settings** (`config/settings/base.py`)

Thêm cấu hình:

**Celery**:

```python
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
```

**Email**:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@hrm.com')
```

### 4. **Config Init** (`config/__init__.py`)

- Import celery app
- Wrapped trong try-except để support environments mà celery chưa cài

### 5. **Chat Models** (`core/chat/models/chat.py`)

Thêm model mới: **ChatActivity**

```python
class ChatActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
    current_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)
```

**Methods**:

- `set_user_online(user, room)`: Đánh dấu user online
- `set_user_offline(user)`: Đánh dấu user offline

### 6. **Chat Admin** (`core/chat/admin.py`)

- Thêm `ChatActivityAdmin` để quản lý trong Django admin
- Display: user, is_online, current_room, last_active

### 7. **Chat Tasks** (`core/chat/tasks.py`) - NEW FILE

**Task 1: `send_email_to_offline_users`**

- Input: message_id
- Logic:
  1. Lấy message từ DB
  2. Tìm tất cả participant trong room
  3. Kiểm tra ai đang offline (ChatActivity.is_online = False)
  4. Gửi email cho những user offline
  5. Retry tối đa 3 lần nếu lỗi
- Email template sử dụng: `templates/email/new_message_notification.html`

**Task 2: `cleanup_offline_status`** (Periodic task)

- Chạy định kỳ (có thể configure via Celery Beat)
- Reset status online của những user không active > 30 phút
- Đảm bảo online status không "stuck" ở true

### 8. **Chat Consumers** (`core/chat/consumers.py`)

**Thay đổi**:

**Trong `connect()` method**:

- Gọi `set_user_online()` để đánh dấu user online

**Trong `disconnect()` method**:

- Gọi `set_user_offline()` để đánh dấu user offline

**Trong `receive()` method**:

- Gọi `send_email_notification()` task khi message được lưu
- Task chạy async qua Celery

**Thêm 3 helper methods**:

- `set_user_online()`: Sync wrapper cho ChatActivity
- `set_user_offline()`: Sync wrapper cho ChatActivity
- `send_email_notification()`: Trigger Celery task

### 9. **Email Template** (`templates/email/new_message_notification.html`) - NEW FILE

HTML template với:

- Tên user
- Tên người gửi
- Tên room
- Nội dung message
- Link để vào room
- Professional styling

### 10. **Docker Compose** (`docker-compose.yml`)

Thêm 2 services mới:

**celery_worker**:

- Chạy command: `celery -A config worker -l info`
- Cùng environment & dependencies với web service

**celery_beat**:

- Chạy command: `celery -A config beat -l info`
- Cho periodic tasks (optional)

### 11. **Documentation**

**CELERY_SETUP.md** - NEW FILE

- Hướng dẫn cài đặt email
- Cách chạy Redis, Celery
- Troubleshooting

**QUICKSTART.md** - UPDATED

- Thêm Bước 5: Setup Celery
- Thêm section Chat System

**.env.example** - UPDATED

- Thêm Celery config
- Thêm Email config

## Cách Hoạt Động

### Flow 1: User gửi message

```
User A (WebSocket Connected) -> Send Message
                                ↓
                    ChatConsumer.receive()
                                ↓
                    ChatMessage created in DB
                                ↓
                    send_email_notification.delay(message_id)
                                ↓
                    Task queued to Redis
```

### Flow 2: Celery Worker xử lý task

```
Celery Worker polls Redis
                                ↓
            Dequeue send_email_to_offline_users task
                                ↓
        Get participants of chat room
                                ↓
    Filter by ChatActivity.is_online = False
                                ↓
        For each offline user:
        - Build email content
        - Send via EMAIL_BACKEND
                                ↓
        Task completed
```

### Flow 3: User status management

```
User 1 joins chat -> connect() -> ChatActivity.set_user_online()
                                           ↓
                            ChatActivity updated (is_online=True)

User 1 leaves chat -> disconnect() -> ChatActivity.set_user_offline()
                                           ↓
                            ChatActivity updated (is_online=False)
```

## Migration

Áp dụng migration để tạo table `chat_activity`:

```bash
python manage.py migrate chat
```

Migration file: `core/chat/migrations/0002_chatactivity.py`

## Startup Steps

### Development

```bash
# Terminal 1: Web server
python manage.py runserver

# Terminal 2: Redis (if not running)
redis-server

# Terminal 3: Celery Worker
celery -A config worker -l info

# Terminal 4 (Optional): Celery Beat
celery -A config beat -l info
```

### Production (Docker)

```bash
docker-compose up -d --build
```

Tất cả services sẽ tự động start (web, celery_worker, celery_beat, db, redis)

## Configuration

### Email Backend

**Development** (Console - default):

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Production** (Gmail):
Cấu hình trong .env

### Redis Connection

**Development**:

```
redis://127.0.0.1:6379/0
```

**Docker**:

```
redis://redis:6379/0
```

## Testing

### Test Email Console Output

```bash
# Trong development, email sẽ print trong Celery worker console
celery -A config worker -l info
```

### Test Task

```bash
python manage.py shell
from core.chat.tasks import send_email_to_offline_users
result = send_email_to_offline_users.delay(1)
result.get()  # Get result
```

### Check Task Queue

```bash
celery -A config inspect active
celery -A config inspect registered
celery -A config inspect stats
```

## Performance Notes

- Email sending chạy async, không block WebSocket
- Retry logic đảm bảo reliability (max 3 retries)
- Redis caching giúp scalability
- Periodic cleanup tránh "stuck" online status

## Security Notes

- App password (bukan account password) dùng cho email
- Email không được gửi cho user đang online
- Celery task secured via broker auth (nếu production)

## Future Enhancements

- Email template templates theo language
- Rate limiting để tránh spam
- Batch emails cùng lúc
- Push notifications (mobile)
- Email preference management
