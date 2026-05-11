# Docker Setup Guide - HRM Chat System

## 📦 Prerequisites

- Docker Desktop installed
- Docker Compose installed
- `.env` file configured (copy from `.env.example`)

---

## 🚀 Quick Start

### 1. **Chuẩn bị Environment Variables**

```bash
# Copy .env.example to .env
cp .env.example .env
```

**Cập nhật `.env` với giá trị thực tế:**

```env
DEBUG=True
SECRET_KEY=your-very-secure-key-here
DB_NAME=hrm_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
ALLOWED_HOSTS=localhost,127.0.0.1,web
```

### 2. **Build và Run Docker Containers**

```bash
# Build images và start services
docker-compose up -d

# Hoặc build lại nếu có thay đổi
docker-compose up -d --build
```

### 3. **Kiểm tra Services**

```bash
# Xem status của tất cả services
docker-compose ps

# Output sẽ tương tự:
# NAME              COMMAND                  SERVICE      STATUS      PORTS
# hrm_postgres      postgres                 db           Up (healthy)  5432/tcp
# hrm_redis         redis-server             redis        Up (healthy)  6379/tcp
# hrm_web           daphne -b 0.0.0.0...    web          Up            0.0.0.0:8000->8000/tcp
```

### 4. **Access Application**

- **Django App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Database**: localhost:5432 (PostgreSQL)
- **Redis**: localhost:6379

---

## 📝 Command Reference

### Start Services

```bash
# Khởi động tất cả services
docker-compose up

# Khởi động background (-d = detached mode)
docker-compose up -d

# Build trước khi khởi động
docker-compose up -d --build
```

### Stop Services

```bash
# Dừng tất cả services
docker-compose stop

# Dừng và xóa containers
docker-compose down

# Xóa containers, images, volumes
docker-compose down -v
```

### View Logs

```bash
# Xem logs tất cả services
docker-compose logs -f

# Xem logs của service cụ thể
docker-compose logs -f web      # Django app
docker-compose logs -f db       # PostgreSQL
docker-compose logs -f redis    # Redis

# Xem logs 100 dòng cuối
docker-compose logs --tail=100 web
```

### Run Django Commands

```bash
# Chạy migrations
docker-compose exec web python manage.py migrate

# Seed dữ liệu ban đầu
docker-compose exec web python manage.py seed_chat

# Tạo superuser
docker-compose exec web python manage.py createsuperuser

# Chạy management command
docker-compose exec web python manage.py <command>
```

### Database Operations

```bash
# Truy cập PostgreSQL shell
docker-compose exec db psql -U postgres -d hrm_db

# Backup database
docker-compose exec db pg_dump -U postgres hrm_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres hrm_db < backup.sql
```

### Shell/Terminal Access

```bash
# SSH vào Django container
docker-compose exec web bash

# SSH vào database container
docker-compose exec db bash

# SSH vào Redis container
docker-compose exec redis sh
```

---

## 🔧 Cấu hình Chi tiết

### Services Trong docker-compose.yml

#### PostgreSQL (db)

```yaml
db:
  image: postgres:15
  ports: 5432:5432
  healthcheck: Kiểm tra connection mỗi 10 giây
  volumes: Lưu data vào postgres_data volume
```

#### Redis (redis)

```yaml
redis:
  image: redis:7-alpine
  ports: 6379:6379
  healthcheck: Kiểm tra ping mỗi 10 giây
  volumes: Lưu data vào redis_data volume
```

#### Django Web (web)

```yaml
web:
  build: Build từ Docker/Dockerfile
  depends_on:
    - db (với health check)
    - redis (với health check)
  volumes:
    - .:/app (live reload code)
    - ./media:/app/media (upload files)
    - ./staticfiles:/app/staticfiles
  command:
    - Migrate database
    - Collect static files
    - Run Daphne ASGI server
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────┐
│            Docker Environment                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌─────────────┐  ┌──────────┐  │
│  │          │  │             │  │          │  │
│  │ Django  │  │ PostgreSQL  │  │  Redis   │  │
│  │ Daphne  │──│             │──│          │  │
│  │ (Port   │  │ (Port 5432) │  │ (Port   │  │
│  │ 8000)   │  │  - hrm_db   │  │ 6379)   │  │
│  │         │  │  - hrm_user │  │         │  │
│  │ WebSocket   │             │  │ Channel │  │
│  │ Support    │             │  │ Layer   │  │
│  │         │  │ volumes:    │  │ volumes │  │
│  │         │  │ postgres_   │  │ redis_  │  │
│  │         │  │ data        │  │ data    │  │
│  │         │  │             │  │         │  │
│  └──────────┘  └─────────────┘  └──────────┘  │
│      ▲         Container networking          │
└─────┼────────────────────────────────────────┘
      │
  Host Machine
  (localhost:8000)
```

---

## ✅ Troubleshooting

### 1. Container không start

```bash
# Xem logs chi tiết
docker-compose logs web

# Rebuild containers
docker-compose down -v
docker-compose up -d --build
```

### 2. Database connection error

```bash
# Kiểm tra health status
docker-compose ps

# Nếu db unhealthy, reset database
docker-compose down -v
docker-compose up -d

# Chạy migrations lại
docker-compose exec web python manage.py migrate
```

### 3. WebSocket connection failed

```bash
# Kiểm tra Redis
docker-compose exec redis redis-cli ping
# Output: PONG

# Kiểm tra container logs
docker-compose logs redis
docker-compose logs web
```

### 4. Static files not loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Kiểm tra volume mount
docker-compose exec web ls -la /app/staticfiles/
```

### 5. Permission denied errors

```bash
# Chạy command với proper user
docker-compose exec -u root web chown -R www-data /app/media
```

---

## 🔐 Security Notes

### Development vs Production

**Development (.env):**

```
DEBUG=True
SECRET_KEY=dev-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Production (cần update):**

```
DEBUG=False
SECRET_KEY=very-long-random-secure-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Environment Variables

- **Không** commit `.env` file vào Git
- **Luôn** sử dụng `.env.example` làm template
- Sử dụng strong passwords cho database

---

## 📈 Performance Tips

1. **Database Optimization**

   ```bash
   # Xem database size
   docker-compose exec db psql -U postgres -d hrm_db -c "SELECT pg_size_pretty(pg_database_size('hrm_db'));"
   ```

2. **Redis Monitoring**

   ```bash
   # Monitor Redis stats
   docker-compose exec redis redis-cli info
   ```

3. **Container Resources**
   ```yaml
   # Thêm resource limits vào docker-compose.yml
   services:
     web:
       deploy:
         resources:
           limits:
             cpus: "1"
             memory: 512M
           reservations:
             cpus: "0.5"
             memory: 256M
   ```

---

## 🚀 Deployment Checklist

- [ ] Update `.env` với production values
- [ ] Set `DEBUG=False`
- [ ] Update `SECRET_KEY` với random string
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Setup SSL certificate
- [ ] Configure backup strategy
- [ ] Setup monitoring/logging
- [ ] Test WebSocket connections
- [ ] Verify database migrations run
- [ ] Test chat functionality

---

## 📚 Thêm Tài liệu

- [Django Channels Documentation](https://channels.readthedocs.io/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Redis Docker](https://hub.docker.com/_/redis)
- [CHAT_SETUP.md](CHAT_SETUP.md) - Chat system setup
- [CHAT_IMPLEMENTATION.md](CHAT_IMPLEMENTATION.md) - Implementation details

---

**Status**: ✅ Ready for Docker deployment  
**Last Updated**: May 7, 2026
