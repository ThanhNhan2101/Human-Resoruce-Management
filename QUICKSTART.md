# HRM System - Quick Start Guide

## 🚀 Bước 1: Cài Đặt

### 1.1 Clone repository

```bash
git clone <repo-url>
cd hrm_project
```

### 1.2 Tạo Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

## 🔧 Bước 2: Khởi Tạo Database

```bash
python manage.py migrate
```

## 📊 Bước 3: Tạo Dữ Liệu Demo

```bash
python scripts/seed_data.py
```

Lệnh này sẽ tạo:

- ✅ 1 superuser: `admin` / `admin123`
- ✅ 12 nhân viên (NV001–NV012) trong 5 phòng ban
- ✅ 12 đơn xin nghỉ phép (PENDING, APPROVED, REJECTED)
- ✅ 360 bản ghi chấm công (30 ngày × 12 nhân viên)

## 🌐 Bước 4: Chạy Development Server

```bash
python manage.py runserver
```

Server sẽ chạy tại: `http://localhost:8000`

## 📝 Đăng Nhập

Sử dụng credentials mặc định:

```
Username: admin
Password: admin123
```

## 🎯 Các Tính Năng Chính

### Dashboard

- Xem thống kê nhân viên (tổng, hoạt động, phòng ban, đang nghỉ)
- Quick links đến các module chính

### Nhân Viên (Employees)

- Xem danh sách tất cả nhân viên
- Thêm / chỉnh sửa / xóa nhân viên
- Filter theo phòng ban, trạng thái
- Xem chi tiết profile từng nhân viên

### Phòng Ban (Departments)

- Xem danh sách phòng ban
- Quản lý cơ cấu tổ chức
- Xem nhân viên theo phòng ban

### Nghỉ Phép (Leaves)

- Xem danh sách tất cả đơn xin nghỉ
- Lọc theo trạng thái (PENDING, APPROVED, REJECTED, CANCELLED)
- Chi tiết từng đơn (ngày, lý do, người phê duyệt)
- Ở chế độ admin, có thể phê duyệt / từ chối đơn

### Chấm Công (Attendance)

- Xem lịch sử chấm công 30 ngày gần nhất
- Xem chi tiết từng ngày (vào/ra, trạng thái)
- Tính toán giờ làm việc tự động

## 🔒 Admin Panel

Truy cập: `http://localhost:8000/admin`

Username: `admin`
Password: `admin123`

Tại Admin Panel có thể:

- Quản lý tất cả employees, departments, leaves, attendance
- Thay đổi mật khẩu
- Xem lịch sử thay đổi dữ liệu

## 📦 Production Deployment

### Chuẩn Bị

1. **Thay đổi SECRET_KEY**:

   ```bash
   # Tạo SECRET_KEY mới
   python manage.py shell
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **Cấu hình .env**:

   ```bash
   SECRET_KEY=<new-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=hrm_db
   DB_USER=postgres
   DB_PASSWORD=<password>
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. **Static Files**:

   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Use Production Server** (Gunicorn + Nginx):

   ```bash
   pip install gunicorn
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```

5. **Backup Database**:
   ```bash
   # Trước khi deploy
   python manage.py dumpdata > backup.json
   ```

## 🐛 Troubleshooting

### Issue: Port 8000 đang bị sử dụng

```bash
# Linux/Mac
python manage.py runserver 8001

# Windows - tìm process sử dụng port
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Database errors

```bash
# Reset migrations
python manage.py migrate --plan  # xem migrations
python manage.py migrate zero    # rollback all
python manage.py migrate         # re-apply all
```

### Issue: Static files không load

```bash
# Collect static files
python manage.py collectstatic --clear --noinput
```

## 📚 Tài Liệu Thêm

- [README.md](README.md) - Tổng quan project
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Chi tiết cấu trúc
- [Django Official Docs](https://docs.djangoproject.com/) - Django documentation

## ✨ Chúc bạn sử dụng vui vẻ!

Nếu có bất kỳ câu hỏi nào, vui lòng tạo issue trên GitHub repo.

- `/admin/` - Admin panel

## Lưu Ý

- Tất cả trang (trừ login) yêu cầu đăng nhập
- Sửa email và password trong `.env` file nếu cần
- Database mặc định là SQLite (`db.sqlite3`)
- Static files được phục vụ từ `/static/` folder
- Media files được lưu trong `/media/` folder

## Troubleshooting

### Lỗi: "No module named 'django'"

```bash
pip install -r requirements.txt
```

### Lỗi: "No such table"

```bash
python manage.py migrate
```

### Lỗi: Port 8000 đã được sử dụng

```bash
python manage.py runserver 8001
```

### Lỗi: Quên password admin

```bash
python manage.py changepassword <username>
```

## Tính Năng Tiếp Theo

- [ ] Export PDF reports
- [ ] Email notifications
- [ ] Salary calculation
- [ ] Performance reviews
- [ ] API documentation
- [ ] Mobile responsive improvements
- [ ] Advanced filtering
- [ ] Bulk operations

---

**Enjoy your HRM System!** 🎉
