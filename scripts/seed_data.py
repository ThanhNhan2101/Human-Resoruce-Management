#!/usr/bin/env python
"""
Django seed script - Tạo dữ liệu demo cho HRM System
Chạy: python scripts/seed_data.py
  hoặc: python manage.py shell < scripts/seed_data.py
"""

from core.attendance.models import Attendance
from core.leaves.models import Leave
from core.employees.models import Employee, Department
from django.contrib.auth import get_user_model
from django.utils import timezone
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal
import random

# Allow running directly: python scripts/seed_data.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()


User = get_user_model()

random.seed(42)
today = timezone.now().date()

# ─────────────────────────────────────────────
# 0. CLEAR existing data
# ─────────────────────────────────────────────
print("🗑  Clearing existing data...")
Attendance.objects.all().delete()
Leave.objects.all().delete()
Employee.objects.all().delete()
Department.objects.all().delete()

# ─────────────────────────────────────────────
# 1. SUPERUSER
# ─────────────────────────────────────────────
print("👤 Creating superuser...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@hrm.local',
        password='admin123',
    )
    print("  - admin / admin123  (superuser created)")
else:
    print("  - admin already exists, skipped")

# ─────────────────────────────────────────────
# 2. DEPARTMENTS
# ─────────────────────────────────────────────
print("🏢 Creating departments...")
dept_data = [
    ('Phòng Nhân Sự',     'Quản lý tuyển dụng, đào tạo và phúc lợi nhân sự'),
    ('Phòng CNTT',        'Phát triển và vận hành hệ thống công nghệ thông tin'),
    ('Phòng Bán Hàng',   'Tìm kiếm khách hàng và thúc đẩy doanh thu'),
    ('Phòng Kế Toán',    'Quản lý tài chính, kế toán và thuế'),
    ('Phòng Marketing',  'Xây dựng thương hiệu và các chiến dịch tiếp thị'),
]
depts = {}
for name, desc in dept_data:
    d, _ = Department.objects.get_or_create(
        name=name, defaults={'description': desc})
    depts[name] = d
    print(f"  - {name}")

# ─────────────────────────────────────────────
# 3. EMPLOYEES
# ─────────────────────────────────────────────
print("👥 Creating employees...")
employee_data = [
    # HR
    dict(first_name='Nguyễn', last_name='Minh Tuấn',  email='tuan.nguyen@hrm.local',
         phone='0912345601', date_of_birth=date(1985, 3, 12), gender='M',
         address='12 Lý Thường Kiệt, Hà Nội', employee_id='NV001',
         department=depts['Phòng Nhân Sự'], position='Trưởng phòng Nhân Sự',
         hire_date=date(2019, 1, 7), status='ACTIVE',
         base_salary=Decimal('22000000'), allowance=Decimal('3000000')),
    dict(first_name='Lê', last_name='Thị Hương',      email='huong.le@hrm.local',
         phone='0912345602', date_of_birth=date(1993, 7, 25), gender='F',
         address='45 Trần Phú, Hà Nội', employee_id='NV002',
         department=depts['Phòng Nhân Sự'], position='Chuyên viên Nhân Sự',
         hire_date=date(2021, 4, 1), status='ACTIVE',
         base_salary=Decimal('14000000'), allowance=Decimal('1500000')),
    # IT
    dict(first_name='Trần', last_name='Văn Khoa',     email='khoa.tran@hrm.local',
         phone='0912345603', date_of_birth=date(1990, 11, 8), gender='M',
         address='33 Nguyễn Trãi, TP.HCM', employee_id='NV003',
         department=depts['Phòng CNTT'], position='Tech Lead',
         hire_date=date(2020, 6, 15), status='ACTIVE',
         base_salary=Decimal('28000000'), allowance=Decimal('4000000')),
    dict(first_name='Phạm', last_name='Thanh Hà',     email='ha.pham@hrm.local',
         phone='0912345604', date_of_birth=date(1996, 2, 14), gender='F',
         address='78 Đinh Tiên Hoàng, TP.HCM', employee_id='NV004',
         department=depts['Phòng CNTT'], position='Backend Developer',
         hire_date=date(2022, 9, 5), status='ACTIVE',
         base_salary=Decimal('18000000'), allowance=Decimal('2000000')),
    dict(first_name='Hoàng', last_name='Đức Minh',    email='minh.hoang@hrm.local',
         phone='0912345605', date_of_birth=date(1998, 5, 20), gender='M',
         address='101 Lê Lợi, Đà Nẵng', employee_id='NV005',
         department=depts['Phòng CNTT'], position='Frontend Developer',
         hire_date=date(2023, 3, 1), status='ACTIVE',
         base_salary=Decimal('16000000'), allowance=Decimal('1500000')),
    dict(first_name='Vũ', last_name='Thị Lan',        email='lan.vu@hrm.local',
         phone='0912345606', date_of_birth=date(1997, 9, 3), gender='F',
         address='55 Bạch Đằng, Đà Nẵng', employee_id='NV006',
         department=depts['Phòng CNTT'], position='QA Engineer',
         hire_date=date(2023, 7, 10), status='ACTIVE',
         base_salary=Decimal('15000000'), allowance=Decimal('1000000')),
    # Sales
    dict(first_name='Đinh', last_name='Văn Long',     email='long.dinh@hrm.local',
         phone='0912345607', date_of_birth=date(1988, 4, 18), gender='M',
         address='22 Hùng Vương, Hải Phòng', employee_id='NV007',
         department=depts['Phòng Bán Hàng'], position='Sales Manager',
         hire_date=date(2018, 8, 20), status='ACTIVE',
         base_salary=Decimal('20000000'), allowance=Decimal('5000000')),
    dict(first_name='Ngô', last_name='Thị Thúy',      email='thuy.ngo@hrm.local',
         phone='0912345608', date_of_birth=date(1999, 12, 1), gender='F',
         address='9 Quang Trung, Hà Nội', employee_id='NV008',
         department=depts['Phòng Bán Hàng'], position='Sales Executive',
         hire_date=date(2024, 2, 1), status='ACTIVE',
         base_salary=Decimal('11000000'), allowance=Decimal('2500000')),
    # Accounting
    dict(first_name='Bùi', last_name='Quốc Dũng',    email='dung.bui@hrm.local',
         phone='0912345609', date_of_birth=date(1987, 6, 30), gender='M',
         address='67 Tràng Tiền, Hà Nội', employee_id='NV009',
         department=depts['Phòng Kế Toán'], position='Kế Toán Trưởng',
         hire_date=date(2017, 5, 10), status='ACTIVE',
         base_salary=Decimal('19000000'), allowance=Decimal('2000000')),
    dict(first_name='Đặng', last_name='Thị Mai',      email='mai.dang@hrm.local',
         phone='0912345610', date_of_birth=date(1994, 8, 22), gender='F',
         address='3 Hoàng Diệu, Hà Nội', employee_id='NV010',
         department=depts['Phòng Kế Toán'], position='Nhân viên Kế Toán',
         hire_date=date(2022, 11, 15), status='ACTIVE',
         base_salary=Decimal('13000000'), allowance=Decimal('1000000')),
    # Marketing
    dict(first_name='Lý', last_name='Văn Hùng',       email='hung.ly@hrm.local',
         phone='0912345611', date_of_birth=date(1992, 1, 9), gender='M',
         address='88 Nam Kỳ Khởi Nghĩa, TP.HCM', employee_id='NV011',
         department=depts['Phòng Marketing'], position='Marketing Manager',
         hire_date=date(2020, 3, 1), status='ACTIVE',
         base_salary=Decimal('21000000'), allowance=Decimal('3500000')),
    dict(first_name='Cao', last_name='Thị Ngọc',      email='ngoc.cao@hrm.local',
         phone='0912345612', date_of_birth=date(2000, 10, 15), gender='F',
         address='14 Võ Thị Sáu, TP.HCM', employee_id='NV012',
         department=depts['Phòng Marketing'], position='Content Creator',
         hire_date=date(2024, 1, 15), status='ACTIVE',
         base_salary=Decimal('12000000'), allowance=Decimal('1000000')),
]

created_employees = []
for data in employee_data:
    emp, created = Employee.objects.get_or_create(
        employee_id=data['employee_id'], defaults=data
    )
    created_employees.append(emp)
    tag = 'created' if created else 'exists'
    print(f"  - {emp.full_name} ({emp.employee_id}) [{tag}]")

hr_manager = created_employees[0]   # NV001 – approves leaves

# ─────────────────────────────────────────────
# 4. LEAVE REQUESTS
# ─────────────────────────────────────────────
print("📋 Creating leave requests...")

leave_scenarios = [
    # (emp_index, days_from_today_start, duration, reason, status, approved_by)
    (1,  5,  3, 'Nghỉ phép năm – đi du lịch gia đình',           'PENDING',  None),
    (2, -10, 2, 'Nghỉ ốm – sốt virus',
     'APPROVED', hr_manager),
    (3,  10, 5, 'Nghỉ phép năm – việc cá nhân',                   'PENDING',  None),
    (4, -20, 1, 'Nghỉ hiếu – đám tang người thân',
     'APPROVED', hr_manager),
    (5,  2,  2, 'Nghỉ bệnh – khám định kỳ',                       'PENDING',  None),
    (6, -5,  3, 'Nghỉ phép năm',
     'APPROVED', hr_manager),
    (7, -30, 2, 'Nghỉ ốm – cảm cúm',
     'REJECTED', hr_manager),
    (8,  15, 4, 'Nghỉ phép năm – về quê',                         'PENDING',  None),
    (9, -15, 1, 'Nghỉ việc riêng',
     'APPROVED', hr_manager),
    (10, 20, 3, 'Nghỉ phép năm – tham dự đám cưới bạn bè',       'PENDING',  None),
    (11, -8, 2, 'Nghỉ ốm – viêm họng',
     'APPROVED', hr_manager),
    (0, -40, 5, 'Nghỉ phép năm – nghỉ dưỡng',
     'APPROVED', hr_manager),
]

for emp_idx, offset_start, duration, reason, status, approved_by in leave_scenarios:
    emp = created_employees[emp_idx]
    start = today + timedelta(days=offset_start)
    end = start + timedelta(days=duration - 1)
    remarks = 'Đã xác nhận' if status == 'APPROVED' else (
              'Không đủ điều kiện' if status == 'REJECTED' else '')
    Leave.objects.create(
        employee=emp,
        start_date=start,
        end_date=end,
        reason=reason,
        status=status,
        approved_by=approved_by,
        remarks=remarks,
    )
    print(f"  - {emp.full_name}: {start} → {end} [{status}]")

# ─────────────────────────────────────────────
# 5. ATTENDANCE (last 30 working days)
# ─────────────────────────────────────────────
print("🕐 Creating attendance records...")


def prev_working_days(ref_date, count):
    """Yield `count` dates going backwards from ref_date, skipping weekends."""
    d = ref_date - timedelta(days=1)
    yielded = 0
    while yielded < count:
        if d.weekday() < 5:   # Mon-Fri
            yield d
            yielded += 1
        d -= timedelta(days=1)


for emp in created_employees:
    records_created = 0
    for work_date in prev_working_days(today, 30):
        # weighted random: mostly PRESENT
        roll = random.random()
        if roll < 0.70:
            status = 'PRESENT'
        elif roll < 0.82:
            status = 'LATE'
        elif roll < 0.90:
            status = 'ABSENT'
        elif roll < 0.95:
            status = 'HALF_DAY'
        else:
            status = 'ON_LEAVE'

        if status in ('PRESENT', 'LATE'):
            late_min = random.randint(5, 45) if status == 'LATE' else 0
            check_in_h = 8 if status == 'PRESENT' else random.choice([9, 10])
            check_in_m = random.randint(
                0, 10) if status == 'PRESENT' else late_min
            check_in = f"{check_in_h:02d}:{check_in_m:02d}:00"
            check_out = f"{random.randint(17, 18):02d}:{random.randint(0, 59):02d}:00"
        elif status == 'HALF_DAY':
            check_in = f"08:{random.randint(0, 15):02d}:00"
            check_out = f"12:{random.randint(0, 30):02d}:00"
        else:
            check_in = check_out = None

        Attendance.objects.get_or_create(
            employee=emp,
            date=work_date,
            defaults=dict(
                check_in_time=check_in,
                check_out_time=check_out,
                status=status,
                notes='',
            )
        )
        records_created += 1
    print(f"  - {emp.full_name}: {records_created} ngày")

# ─────────────────────────────────────────────
# 6. SUMMARY
# ─────────────────────────────────────────────
print("\n✅ Seed data hoàn tất!")
print(f"   Nhân viên    : {Employee.objects.count()}")
print(f"   Phòng ban    : {Department.objects.count()}")
print(f"   Đơn nghỉ    : {Leave.objects.count()}")
print(f"   Chấm công    : {Attendance.objects.count()}")
print(f"\n   Đăng nhập   : admin / admin123")
