# HRM System - Quick Start Guide

## Bước 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Bước 2: Run Migrations

```bash
python manage.py migrate
```

## Bước 3: Create Superuser

```bash
python manage.py createsuperuser
```

## Bước 4: Create Demo Data (Optional)

Mở Django shell:

```bash
python manage.py shell
```

Chạy lệnh sau:

```python
from core.employees.models import Employee, Department, Position
from django.utils import timezone
from datetime import date

# Tạo phòng ban
hr_dept = Department.objects.create(
    name='Phòng Nhân Sự',
    description='Bộ phận quản lý nhân sự'
)

it_dept = Department.objects.create(
    name='Phòng CNTT',
    description='Bộ phận công nghệ thông tin'
)

sales_dept = Department.objects.create(
    name='Phòng Bán Hàng',
    description='Bộ phận kinh doanh'
)

# Tạo chức vụ
pos1 = Position.objects.create(
    name='Nhân viên',
    department=hr_dept
)

pos2 = Position.objects.create(
    name='Developer',
    department=it_dept
)

pos3 = Position.objects.create(
    name='Sales Executive',
    department=sales_dept
)

# Tạo nhân viên
emp1 = Employee.objects.create(
    first_name='Nguyễn',
    last_name='Văn A',
    email='a.nguyen@hrm.local',
    phone='+84912345678',
    date_of_birth=date(1995, 5, 15),
    gender='M',
    address='123 Đường A, Hà Nội',
    employee_id='NV001',
    department=hr_dept,
    position=pos1,
    hire_date=date(2022, 1, 15),
    base_salary=10000000,
    allowance=500000
)

emp2 = Employee.objects.create(
    first_name='Trần',
    last_name='Thị B',
    email='b.tran@hrm.local',
    phone='+84987654321',
    date_of_birth=date(1998, 8, 20),
    gender='F',
    address='456 Đường B, TPHCM',
    employee_id='NV002',
    department=it_dept,
    position=pos2,
    hire_date=date(2023, 3, 1),
    base_salary=15000000,
    allowance=1000000
)

emp3 = Employee.objects.create(
    first_name='Phạm',
    last_name='Văn C',
    email='c.pham@hrm.local',
    phone='+84977777777',
    date_of_birth=date(1996, 2, 28),
    gender='M',
    address='789 Đường C, Đà Nẵng',
    employee_id='NV003',
    department=sales_dept,
    position=pos3,
    hire_date=date(2021, 6, 15),
    base_salary=12000000,
    allowance=2000000
)

print("Tạo dữ liệu demo thành công!")
```

Nhấp Ctrl+D hoặc Cmd+D để thoát shell.

## Bước 5: Run Development Server

```bash
python manage.py runserver
```

## Bước 6: Access Application

- **Admin Panel**: http://localhost:8000/admin
- **Main App**: http://localhost:8000

Đăng nhập bằng tài khoản superuser.

## Cấu Trúc URL Chính

- `/` - Trang chủ
- `/dashboard/` - Bảng điều khiển
- `/dashboard/employees/` - Danh sách nhân viên
- `/dashboard/employees/create/` - Thêm nhân viên
- `/dashboard/employees/<id>/` - Chi tiết nhân viên
- `/dashboard/employees/<id>/edit/` - Chỉnh sửa
- `/dashboard/employees/<id>/delete/` - Xóa
- `/dashboard/departments/` - Danh sách phòng ban
- `/leaves/` - Danh sách nghỉ phép
- `/leaves/create/` - Đăng ký nghỉ phép
- `/leaves/<id>/` - Chi tiết nghỉ phép
- `/attendance/` - Danh sách chấm công
- `/attendance/daily/` - Chấm công ngày
- `/attendance/create/` - Thêm chấm công
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
