"""
Shared pytest fixtures and configuration for HRM System tests.
"""
from core.attendance.models import Attendance
from core.leaves.models import Leave
from core.employees.models import Employee, Department
import os
import django
from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()


User = get_user_model()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PYTEST CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "django_db: mark test as needing database access"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DEPARTMENT FIXTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@pytest.fixture
def department(db):
    """Create a test department."""
    return Department.objects.create(
        name="Engineering",
        description="Engineering department for software development"
    )


@pytest.fixture
def hr_department(db):
    """Create a test HR department."""
    return Department.objects.create(
        name="Human Resources",
        description="HR department"
    )


@pytest.fixture
def departments(db, department, hr_department):
    """Create multiple departments."""
    return [department, hr_department]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EMPLOYEE FIXTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@pytest.fixture
def employee(db, department):
    """Create a test employee."""
    return Employee.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="+1234567890",
        date_of_birth=date(1990, 1, 15),
        gender="M",
        address="123 Main St, City",
        employee_id="EMP001",
        department=department,
        position="Software Engineer",
        hire_date=date(2020, 1, 1),
        status="ACTIVE",
        base_salary=Decimal("50000.00"),
        allowance=Decimal("5000.00")
    )


@pytest.fixture
def employee2(db, department):
    """Create a second test employee."""
    return Employee.objects.create(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        phone="+0987654321",
        date_of_birth=date(1992, 5, 20),
        gender="F",
        address="456 Oak Ave, City",
        employee_id="EMP002",
        department=department,
        position="Senior Developer",
        hire_date=date(2018, 6, 15),
        status="ACTIVE",
        base_salary=Decimal("60000.00"),
        allowance=Decimal("7000.00")
    )


@pytest.fixture
def employees(db, employee, employee2):
    """Create multiple test employees."""
    return [employee, employee2]


@pytest.fixture
def inactive_employee(db, department):
    """Create an inactive employee."""
    return Employee.objects.create(
        first_name="Bob",
        last_name="Inactive",
        email="bob.inactive@example.com",
        phone="+1111111111",
        date_of_birth=date(1988, 3, 10),
        gender="M",
        address="789 Pine St, City",
        employee_id="EMP003",
        department=department,
        position="Contractor",
        hire_date=date(2015, 1, 1),
        status="INACTIVE",
        base_salary=Decimal("40000.00"),
        allowance=Decimal("3000.00")
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LEAVE FIXTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@pytest.fixture
def leave_pending(db, employee):
    """Create a pending leave request."""
    return Leave.objects.create(
        employee=employee,
        start_date=date.today() + timedelta(days=7),
        end_date=date.today() + timedelta(days=10),
        reason="Annual vacation",
        status="PENDING"
    )


@pytest.fixture
def leave_approved(db, employee, employee2):
    """Create an approved leave request."""
    return Leave.objects.create(
        employee=employee,
        start_date=date.today() - timedelta(days=10),
        end_date=date.today() - timedelta(days=7),
        reason="Sick leave",
        status="APPROVED",
        approved_by=employee2
    )


@pytest.fixture
def leave_rejected(db, employee, employee2):
    """Create a rejected leave request."""
    return Leave.objects.create(
        employee=employee,
        start_date=date.today() + timedelta(days=15),
        end_date=date.today() + timedelta(days=20),
        reason="Personal leave",
        status="REJECTED",
        remarks="Insufficient notice period",
        approved_by=employee2
    )


@pytest.fixture
def leaves(db, leave_pending, leave_approved, leave_rejected):
    """Create multiple leaves."""
    return [leave_pending, leave_approved, leave_rejected]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ATTENDANCE FIXTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@pytest.fixture
def attendance_present(db, employee):
    """Create a present attendance record."""
    from datetime import time
    return Attendance.objects.create(
        employee=employee,
        date=date.today(),
        check_in_time=time(9, 0),
        check_out_time=time(17, 0),
        status="PRESENT",
        notes="Regular working day"
    )


@pytest.fixture
def attendance_late(db, employee):
    """Create a late attendance record."""
    from datetime import time
    return Attendance.objects.create(
        employee=employee,
        date=date.today() - timedelta(days=1),
        check_in_time=time(9, 30),
        check_out_time=time(17, 30),
        status="LATE"
    )


@pytest.fixture
def attendance_absent(db, employee2):
    """Create an absent attendance record."""
    return Attendance.objects.create(
        employee=employee2,
        date=date.today() - timedelta(days=2),
        status="ABSENT"
    )


@pytest.fixture
def attendance_half_day(db, employee):
    """Create a half-day attendance record."""
    from datetime import time
    return Attendance.objects.create(
        employee=employee,
        date=date.today() - timedelta(days=3),
        check_in_time=time(9, 0),
        check_out_time=time(12, 0),
        status="HALF_DAY",
        notes="Left early for medical appointment"
    )


@pytest.fixture
def attendances(db, attendance_present, attendance_late, attendance_absent, attendance_half_day):
    """Create multiple attendance records."""
    return [attendance_present, attendance_late, attendance_absent, attendance_half_day]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# USER FIXTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )


@pytest.fixture
def regular_user(db):
    """Create a regular user."""
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpass123'
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLIENT FIXTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@pytest.fixture
def client():
    """Create a Django test client."""
    return Client()


@pytest.fixture
def auth_client(client, admin_user):
    """Create an authenticated Django test client."""
    client.login(username='admin', password='admin123')
    return client
