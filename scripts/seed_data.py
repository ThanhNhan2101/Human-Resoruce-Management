#!/usr/bin/env python
"""
Django seed script - Tạo dữ liệu demo cho HRM System
Chạy: python manage.py shell < scripts/seed_data.py
"""

from django.utils import timezone
from core.attendance.models import Attendance
from core.leaves.models import Leave, LeaveType
from core.employees.models import Employee, Department, Position
import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()


# Clear existing data (optional)
print("Clearing existing data...")
Employee.objects.all().delete()
Department.objects.all().delete()
Position.objects.all().delete()
LeaveType.objects.all().delete()

# Create Departments
print("Creating departments...")
departments = {
    'hr': Department.objects.create(
        name='Phòng Nhân Sự',
        description='Bộ phận quản lý nhân sự'
    ),
    'it': Department.objects.create(
        name='Phòng CNTT',
        description='Bộ phận công nghệ thông tin'
    ),
    'sales': Department.objects.create(
        name='Phòng Bán Hàng',
        description='Bộ phận kinh doanh'
    ),
    'accounting': Department.objects.create(
        name='Phòng Kế Toán',
        description='Bộ phận tài chính kế toán'
    ),
}

# Create Positions
print("Creating positions...")
positions = {}
for dept_key, dept in departments.items():
    if dept_key == 'hr':
        positions['hr_manager'] = Position.objects.create(
            name='Trưởng phòng HR',
            department=dept
        )
        positions['hr_staff'] = Position.objects.create(
            name='Nhân viên HR',
            department=dept
        )
    elif dept_key == 'it':
        positions['dev_lead'] = Position.objects.create(
            name='Tech Lead',
            department=dept
        )
        positions['dev'] = Position.objects.create(
            name='Developer',
            department=dept
        )
        positions['qa'] = Position.objects.create(
            name='QA Engineer',
            department=dept
        )
    elif dept_key == 'sales':
        positions['sales_manager'] = Position.objects.create(
            name='Sales Manager',
            department=dept
        )
        positions['sales_exec'] = Position.objects.create(
            name='Sales Executive',
            department=dept
        )
    elif dept_key == 'accounting':
        positions['accountant'] = Position.objects.create(
            name='Nhân viên Kế Toán',
            department=dept
        )

# Create Employees
print("Creating employees...")
employees = [
    {
        'first_name': 'Nguyễn',
        'last_name': 'Văn A',
        'email': 'a.nguyen@hrm.local',
        'phone': '+84912345678',
        'date_of_birth': date(1995, 5, 15),
        'gender': 'M',
        'address': '123 Đường Nguyễn Huệ, Hà Nội',
        'employee_id': 'NV001',
        'department': departments['hr'],
        'position': positions['hr_manager'],
        'hire_date': date(2022, 1, 15),
        'base_salary': 15000000,
        'allowance': 1000000,
    },
    {
        'first_name': 'Trần',
        'last_name': 'Thị B',
        'email': 'b.tran@hrm.local',
        'phone': '+84987654321',
        'date_of_birth': date(1998, 8, 20),
        'gender': 'F',
        'address': '456 Đường Lê Lợi, TPHCM',
        'employee_id': 'NV002',
        'department': departments['it'],
        'position': positions['dev_lead'],
        'hire_date': date(2023, 3, 1),
        'base_salary': 18000000,
        'allowance': 2000000,
    },
    {
        'first_name': 'Phạm',
        'last_name': 'Văn C',
        'email': 'c.pham@hrm.local',
        'phone': '+84977777777',
        'date_of_birth': date(1996, 2, 28),
        'gender': 'M',
        'address': '789 Đường Trần Hưng Đạo, Đà Nẵng',
        'employee_id': 'NV003',
        'department': departments['sales'],
        'position': positions['sales_manager'],
        'hire_date': date(2021, 6, 15),
        'base_salary': 16000000,
        'allowance': 3000000,
    },
    {
        'first_name': 'Hoàng',
        'last_name': 'Thị D',
        'email': 'd.hoang@hrm.local',
        'phone': '+84988888888',
        'date_of_birth': date(2000, 3, 10),
        'gender': 'F',
        'address': '321 Đường Cách Mạng Tháng 8, Quảng Ninh',
        'employee_id': 'NV004',
        'department': departments['it'],
        'position': positions['dev'],
        'hire_date': date(2023, 9, 1),
        'base_salary': 13000000,
        'allowance': 1000000,
    },
    {
        'first_name': 'Võ',
        'last_name': 'Văn E',
        'email': 'e.vo@hrm.local',
        'phone': '+84966666666',
        'date_of_birth': date(1994, 11, 5),
        'gender': 'M',
        'address': '654 Đường Hàng Tràu, Hà Nội',
        'employee_id': 'NV005',
        'department': departments['accounting'],
        'position': positions['accountant'],
        'hire_date': date(2022, 7, 20),
        'base_salary': 12000000,
        'allowance': 500000,
    },
    {
        'first_name': 'Đinh',
        'last_name': 'Thị F',
        'email': 'f.dinh@hrm.local',
        'phone': '+84944444444',
        'date_of_birth': date(1999, 1, 15),
        'gender': 'F',
        'address': '987 Đường Bạch Đằng, Hải Phòng',
        'employee_id': 'NV006',
        'department': departments['sales'],
        'position': positions['sales_exec'],
        'hire_date': date(2024, 1, 10),
        'base_salary': 10000000,
        'allowance': 2000000,
    },
]

created_employees = []
for emp_data in employees:
    emp = Employee.objects.create(**emp_data)
    created_employees.append(emp)
    print(f"  - Created: {emp.full_name} ({emp.employee_id})")

# Create Leave Types
print("Creating leave types...")
leave_types = [
    LeaveType.objects.create(
        name='Phép năm',
        days_per_year=12,
        is_paid=True,
        description='Nghỉ phép hàng năm'
    ),
    LeaveType.objects.create(
        name='Phép bệnh',
        days_per_year=5,
        is_paid=True,
        description='Nghỉ phép khi bệnh'
    ),
    LeaveType.objects.create(
        name='Phép hưởng lương',
        days_per_year=20,
        is_paid=True,
        description='Phép hưởng lương đầy đủ'
    ),
    LeaveType.objects.create(
        name='Phép không lương',
        days_per_year=10,
        is_paid=False,
        description='Phép không hưởng lương'
    ),
]

# Create some Leave requests
print("Creating leave requests...")
for emp in created_employees[:3]:
    Leave.objects.create(
        employee=emp,
        leave_type=leave_types[0],
        start_date=timezone.now().date() + timedelta(days=5),
        end_date=timezone.now().date() + timedelta(days=7),
        reason='Nghỉ phép hàng năm',
        status='PENDING'
    )
    print(f"  - Created leave for: {emp.full_name}")

# Create Attendance records
print("Creating attendance records...")
today = timezone.now().date()
for emp in created_employees:
    for i in range(1, 21):  # Last 20 days
        att_date = today - timedelta(days=i)
        status = random.choice(
            ['PRESENT', 'PRESENT', 'PRESENT', 'LATE', 'ABSENT'])

        check_in = f"{random.randint(7, 9):02d}:{random.randint(0, 59):02d}" if status in [
            'PRESENT', 'LATE'] else None
        check_out = f"{random.randint(17, 18):02d}:{random.randint(0, 59):02d}" if status == 'PRESENT' else None

        Attendance.objects.create(
            employee=emp,
            date=att_date,
            check_in_time=check_in,
            check_out_time=check_out,
            status=status,
            notes='Auto generated demo data' if i % 5 == 0 else ''
        )
    print(f"  - Created 20 attendance records for: {emp.full_name}")

print("\n✅ Seed data created successfully!")
print(f"Total Employees: {Employee.objects.count()}")
print(f"Total Departments: {Department.objects.count()}")
print(f"Total Positions: {Position.objects.count()}")
print(f"Total Leave Requests: {Leave.objects.count()}")
print(f"Total Attendance Records: {Attendance.objects.count()}")
