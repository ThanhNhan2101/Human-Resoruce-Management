# Tính Năng Đăng Nhập Qua Username/Password - Tóm Tắt Triển Khai

## Mô Tả Tính Năng

Admin có thể tạo user nhân viên với username và password. Nhân viên sau đó có thể sử dụng những credentials này để đăng nhập vào hệ thống.

## Các Thay Đổi Được Thực Hiện

### 1. **Employee Model** (`core/employees/models/employee.py`)

- Thêm import: `from django.contrib.auth.models import User`
- Thêm field mới:
  ```python
  user = models.OneToOneField(
      User,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='employee'
  )
  ```
- Tạo migration: `0003_employee_user.py`

### 2. **EmployeeForm** (`core/employees/views/employee_views.py`)

- Thêm hai custom fields:
  - `username`: CharField (optional, required cho creation)
  - `password`: CharField with PasswordInput widget (optional, required cho creation)
- Fields này không được lưu trữ trực tiếp trên Employee model, mà được sử dụng tạo User account

### 3. **EmployeeService** (`core/employees/usecase/services/employee_services.py`)

- **`create()` method**:
  - Extract `username` và `password` từ input dict
  - Tạo Django User account với `User.objects.create_user()`
  - Link User vào Employee thông qua field `user`
  - Kiểm tra duplicate username
- **`update()` method**:
  - Cho phép cập nhật User account nếu username/password được cung cấp
  - Nếu Employee không có User, tạo User mới
  - Sử dụng `set_password()` để hash password
- **`delete()` method**:
  - Xóa cả Employee và associated User account

### 4. **EmployeeCreateView** (`core/employees/views/employee_views.py`)

- Thêm validation để yêu cầu username và password khi tạo employee mới
- Return form errors nếu thiếu credentials

### 5. **LoginForm** (`config/forms.py`)

- Không cần thay đổi - đã hỗ trợ username/password authentication qua Django AuthenticationForm

## Workflow

### Tạo Nhân Viên Mới (Admin)

1. Admin điền form tạo nhân viên với tất cả fields
2. Điền `username` và `password` (bắt buộc)
3. Form được validate
4. EmployeeService tạo:
   - Django User account với username/password
   - Employee record link tới User account

### Đăng Nhập (Nhân Viên)

1. Nhân viên truy cập trang login
2. Nhập username và password
3. LoginForm xác thực thông qua Django auth system
4. User được redirect tới dashboard

### Cập Nhật Thông Tin Nhân Viên

1. Admin có thể update Employee fields
2. Nếu muốn thay đổi credentials:
   - Cập nhật username/password trong form
   - EmployeeService sẽ update User account

### Xóa Nhân Viên

1. Admin xóa Employee
2. Associated User account cũng bị xóa

## Cách Chạy Migration

```bash
# Tạo migration (đã thực hiện)
python manage.py makemigrations employees

# Áp dụng migration vào database
python manage.py migrate
```

**Lưu ý**: Để chạy migration, đảm bảo:

- Database (PostgreSQL) đang chạy
- Environment variables được set đúng (.env file)
- Hoặc sử dụng SQLite bằng cách modify settings

## Kiểm Tra Tính Năng

### 1. Tạo Nhân Viên Mới

- Truy cập `/dashboard/employees/create/`
- Điền form với username và password
- Kiểm tra Employee record và User account đã được tạo

### 2. Đăng Nhập

- Truy cập trang login
- Sử dụng username/password vừa tạo
- Kiểm tra user được authenticate thành công

### 3. Xem Employee

- Truy cập `/dashboard/employees/`
- Kiểm tra employee có field `user` liên kết tới User account

## Database Queries

Xem relationship giữa Employee và User:

```python
# Từ Employee
employee = Employee.objects.get(pk=1)
user = employee.user  # Access User account

# Từ User
user = User.objects.get(username='username')
employee = user.employee  # Access Employee record
```

## Security Notes

- Password được hash bằng Django's password hasher (PBKDF2 by default)
- OneToOneField đảm bảo mỗi Employee chỉ có một User account
- User account có thể null/blank cho backwards compatibility

## Các Files Được Thay Đổi

1. ✅ `core/employees/models/employee.py` - Thêm User field
2. ✅ `core/employees/migrations/0003_employee_user.py` - Migration file (auto-generated)
3. ✅ `core/employees/views/employee_views.py` - Cập nhật EmployeeForm và Views
4. ✅ `core/employees/usecase/services/employee_services.py` - Cập nhật Service logic

## Bước Tiếp Theo (Optional)

1. Update Admin interface để display User link
2. Thêm password change view cho employee
3. Thêm password reset functionality
4. Thêm User activation email
5. Thêm audit logging cho user creation/deletion
