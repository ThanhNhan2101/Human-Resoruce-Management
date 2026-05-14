# Celery & Email Notification Setup

## Overview

Hệ thống đã được cấu hình để gửi email thông báo cho những user offline khi có tin nhắn mới trong chat room.

## Yêu cầu

- Redis (Broker & Result Backend)
- Celery Worker chạy ở background

## Cấu hình Email

### Gmail (Recommended)

Thêm các biến environment vào `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@hrm.com
```

**Lưu ý**: Gmail yêu cầu "App Password" thay vì regular password. Bật 2FA và tạo app password tại: https://myaccount.google.com/apppasswords

### Other Email Services

Có thể sử dụng các dịch vụ khác như SendGrid, Mailgun, etc. Chỉ cần cập nhật settings tương ứng.

## Cấu hình Redis

### Local Setup (Development)

Đảm bảo Redis chạy:

```bash
redis-server
```

### Docker Setup

Redis đã được cấu hình trong `docker-compose.yml`

## Chạy Celery

### Development Mode

Mở terminal mới và chạy:

```bash
# Terminal 1: Django Dev Server
python manage.py runserver

# Terminal 2: Celery Worker
celery -A config worker -l info

# Terminal 3 (Optional): Celery Beat (Scheduler - cho periodic tasks)
celery -A config beat -l info
```

### Production Mode (Docker)

Celery worker được chạy tự động trong docker-compose:

```bash
docker-compose up -d --build
```

## Cấu hình trong settings/base.py

```python
# Celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

## Cách hoạt động

1. **User Online/Offline Tracking**:
   - Khi user kết nối WebSocket → Đánh dấu user là online
   - Khi user disconnect → Đánh dấu user là offline
   - Bảng `chat_activity` lưu trạng thái này

2. **Gửi Email khi có Message**:
   - Khi message được gửi trong room
   - Hệ thống tìm tất cả participant trong room
   - Nếu participant đang offline → Queue email notification task
   - Celery Worker xử lý task và gửi email

3. **Periodic Cleanup** (Optional):
   - Task `cleanup_offline_status` chạy định kỳ
   - Reset trạng thái online của những user không active > 30 phút
   - Cấu hình trong Celery Beat

## Testing

### Test Email Sending (Development)

Nếu chưa cấu hình email thật, sử dụng Console Email Backend:

```python
# settings/base.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails sẽ print trong console thay vì gửi thực tế.

### Test Celery Task

```bash
python manage.py shell

from core.chat.tasks import send_email_to_offline_users
result = send_email_to_offline_users.delay(1)  # message_id = 1
result.get()  # Check result
```

### Check Celery Worker Status

```bash
celery -A config inspect active
celery -A config inspect registered
```

## Migration

Áp dụng migration cho model ChatActivity:

```bash
python manage.py migrate chat
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'celery'"

- Cài đặt packages: `pip install -r requirements.txt`

### "ConnectionRefusedError: [Errno 111] Connection refused"

- Redis không chạy
- Chạy: `redis-server`

### Email không được gửi

- Kiểm tra Celery Worker chạy hay không
- Xem logs: `celery -A config worker -l debug`
- Kiểm tra email settings trong .env

### User vẫn nhận email khi đang online

- Kiểm tra logic trong `send_email_to_offline_users` task
- Đảm bảo `ChatActivity.set_user_online()` được gọi khi user connect

## Files Liên Quan

- `config/celery.py` - Celery configuration
- `core/chat/tasks.py` - Email notification tasks
- `core/chat/models/chat.py` - ChatActivity model
- `core/chat/consumers.py` - WebSocket consumer (online/offline tracking)
- `templates/email/new_message_notification.html` - Email template
