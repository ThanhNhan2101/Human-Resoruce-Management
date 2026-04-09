# HRM System - Hệ Thống Quản Lý Nhân Sự

Một ứng dụng Django hoàn chỉnh để quản lý nhân sự, includinghông tin nhân viên, nghỉ phép, chấm công, và nhiều tính năng khác.

## 🚀 Tính Năng Chính

- **Quản lý nhân viên**: Thêm, sửa, xóa thông tin nhân viên
- **Quản lý phòng ban & chức vụ**: Tổ chức cơ cấu công ty
- **Quản lý nghỉ phép**: Đăng ký, phê duyệt, từ chối đơn nghỉ phép
- **Quản lý chấm công**: Ghi nhận thời gian vào/ra, tính giờ làm
- **Bảng điều khiển**: Thống kê tổng quan về nhân sự
- **Báo cáo**: Xuất dữ liệu nhân viên
- **Admin Panel**: Quản trị toàn hệ thống

## 📋 Yêu Cầu

- Python 3.8+
- Django 5.2
- SQLite (default) hoặc PostgreSQL

## 💻 Cài Đặt

### 1. Clone Project

```bash
git clone <repo-url>
cd hrm_project
```

### 2. Tạo Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu Hình .env

```bash
# Copy file .env.example thành .env (nếu có)
# Hoặc sử dụng .env mặc định
```

### 5. Tạo Migrations

```bash
python manage.py makemigrations
```

### 6. Chạy Migrations

```bash
python manage.py migrate
```

### 7. Tạo Superuser (Admin)

```bash
python manage.py createsuperuser
# Nhập email, password
```

### 8. Tạo Dữ Liệu Demo (Optional)

```bash
python manage.py shell < scripts/seed_data.py
```

### 9. Chạy Development Server

```bash
python manage.py runserver
```

Truy cập: `http://localhost:8000`

## 📁 Cấu Trúc Project

```
hrm_project/
├── config/              # Cấu hình Django
│   ├── settings/
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                # Các ứng dụng chính
│   ├── employees/       # Quản lý nhân viên
│   ├── leaves/          # Quản lý nghỉ phép
│   └── attendance/      # Quản lý chấm công
├── common/              # Các hàm/model dùng chung
├── templates/           # Django templates
├── static/              # CSS, JS, images
├── manage.py
├── requirements.txt
└── .env
```

## 🔐 Đăng Nhập

### Admin Panel

- URL: `http://localhost:8000/admin`
- Username: (superuser name)
- Password: (superuser password)

### Ứng dụng

- URL: `http://localhost:8000`
- Sử dụng tài khoản superuser hoặc tạo tài khoản khác

## 📖 Hướng Dẫn Sử Dụng

### 1. Quản Lý Nhân Viên

1. Vào **Nhân viên** từ menu sidebar
2. Nhấp **Thêm nhân viên mới**
3. Điền thông tin cá nhân và tuyển dụng
4. Nhấp **Thêm**

### 2. Quản Lý Phòng Ban

1. Vào **Phòng ban** từ menu sidebar
2. Xem danh sách phòng ban hiện có
3. Để thêm phòng ban, vào **Admin Panel** > **Phòng ban** > **Thêm phòng ban**

### 3. Đăng Ký Nghỉ Phép

1. Vào **Nghỉ phép** từ menu sidebar
2. Nhấp **Đăng ký nghỉ phép**
3. Chọn nhân viên, loại phép, ngày bắt đầu/kết thúc
4. Nhấp **Đăng ký**

### 4. Chấm Công

1. Vào **Chấm công** từ menu sidebar
2. Nhấp **Chấm công hôm nay**
3. Cập nhật thời gian vào/ra cho từng nhân viên
4. Nhấp **Lưu chấm công**

### 5. Phê Duyệt Đơn Nghỉ Phép

1. Vào **Nghỉ phép**
2. Nhấp vào đơn cần phê duyệt
3. Nhấp **Phê duyệt** hoặc **Từ chối**

## 🛠️ Phát Triển Thêm

### Thêm Model Mới

1. Tạo model trong `models/`
2. Chạy `python manage.py makemigrations`
3. Chạy `python manage.py migrate`

### Thêm View Mới

1. Tạo class view trong `views/`
2. Thêm URL pattern trong `urls.py`
3. Tạo template HTML trong `templates/`

### Thêm API Endpoints

Sử dụng Django REST Framework để thêm API endpoints:

```python
from rest_framework import serializers, viewsets
from core.employees.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
```

## 📊 Models

### Employee

```python
- employee_id (CharField)
- first_name, last_name (CharField)
- email (EmailField)
- phone (CharField)
- date_of_birth (DateField)
- gender (CharField)
- address (TextField)
- department (ForeignKey)
- position (ForeignKey)
- hire_date (DateField)
- status (CharField)
- base_salary, allowance (DecimalField)
- avatar (ImageField)
```

### Leave

```python
- employee (ForeignKey)
- leave_type (ForeignKey)
- start_date, end_date (DateField)
- reason (TextField)
- status (CharField)
- approved_by (ForeignKey)
- remarks (TextField)
```

### Attendance

```python
- employee (ForeignKey)
- date (DateField)
- check_in_time, check_out_time (TimeField)
- status (CharField)
- notes (TextField)
```

## 🔒 Bảo Mật

- Sử dụng Django authentication
- CSRF protection cho tất cả forms
- SQLi prevention thông qua Django ORM
- XSS protection từ Jinja2 template engine

## 📝 Lưu Ý

- Thay đổi `SECRET_KEY` trong production
- Đặt `DEBUG=False` trong production
- Sử dụng PostgreSQL thay vì SQLite trong production
- Cấu hình ALLOWED_HOSTS cho domain của bạn

## 🤝 Contribute

Rất hoan nghênh các pull request để cải thiện project!

## 📄 License

MIT License

## 📞 Hỗ Trợ

Để báo cáo bug hoặc đề xuất tính năng, vui lòng tạo issue trên GitHub.

---

**Tác giả**: Generated for HR Management System  
**Ngày tạo**: 2024  
**Phiên bản**: 1.0.0
