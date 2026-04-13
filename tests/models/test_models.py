"""
Comprehensive Model Tests for HRM System.
Tests for Department, Employee, Leave, and Attendance models.
"""
from datetime import date, timedelta, time
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from core.employees.models import Employee, Department
from core.leaves.models import Leave
from core.attendance.models import Attendance


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DEPARTMENT MODEL TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestDepartmentModel:
    """Test cases for Department model."""

    def test_department_creation(self, db):
        """Test creating a department."""
        dept = Department.objects.create(
            name="Engineering",
            description="Engineering department"
        )
        assert dept.id is not None
        assert dept.name == "Engineering"
        assert dept.description == "Engineering department"
        assert dept.created_at is not None
        assert dept.updated_at is not None

    def test_department_str_representation(self, department):
        """Test department string representation."""
        assert str(department) == "Engineering"

    def test_department_name_unique(self, department, db):
        """Test that department names are unique."""
        with pytest.raises(IntegrityError):
            Department.objects.create(
                name="Engineering",
                description="Duplicate department"
            )

    def test_department_description_optional(self, db):
        """Test that department description is optional."""
        dept = Department.objects.create(name="Sales")
        assert dept.description is None

    def test_department_ordering(self, db):
        """Test that departments are ordered by name."""
        Department.objects.create(name="Zebra Department")
        Department.objects.create(name="Alpha Department")
        Department.objects.create(name="Beta Department")

        depts = list(Department.objects.all())
        assert depts[0].name == "Alpha Department"
        assert depts[1].name == "Beta Department"
        assert depts[2].name == "Zebra Department"

    def test_department_employees_relationship(self, department, employee):
        """Test department-employees relationship."""
        assert department.employees.count() == 1
        assert department.employees.first() == employee


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EMPLOYEE MODEL TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestEmployeeModel:
    """Test cases for Employee model."""

    def test_employee_creation(self, db, department):
        """Test creating an employee."""
        emp = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+1234567890",
            date_of_birth=date(1990, 1, 15),
            gender="M",
            address="123 Main St",
            employee_id="EMP001",
            department=department,
            position="Developer",
            hire_date=date(2020, 1, 1),
            status="ACTIVE",
            base_salary=Decimal("50000.00"),
            allowance=Decimal("5000.00")
        )
        assert emp.id is not None
        assert emp.first_name == "John"
        assert emp.full_name == "John Doe"

    def test_employee_email_unique(self, employee, db):
        """Test that employee emails are unique."""
        with pytest.raises(IntegrityError):
            Employee.objects.create(
                first_name="Duplicate",
                last_name="Email",
                email="john.doe@example.com",  # Same as fixture
                phone="+9999999999",
                date_of_birth=date(1992, 5, 20),
                gender="F",
                address="456 Oak Ave",
                employee_id="EMP999",
                department=employee.department,
                position="Developer",
                hire_date=date(2021, 1, 1),
                status="ACTIVE",
                base_salary=Decimal("45000.00")
            )

    def test_employee_id_unique(self, employee, db, department):
        """Test that employee IDs are unique."""
        with pytest.raises(IntegrityError):
            Employee.objects.create(
                first_name="Another",
                last_name="Person",
                email="another@example.com",
                phone="+8888888888",
                date_of_birth=date(1993, 7, 10),
                gender="M",
                address="789 Pine St",
                employee_id="EMP001",  # Same as fixture
                department=department,
                position="Manager",
                hire_date=date(2019, 1, 1),
                status="ACTIVE",
                base_salary=Decimal("55000.00")
            )

    def test_employee_phone_validation(self, db, department):
        """Test phone number validation."""
        with pytest.raises(ValidationError):
            emp = Employee(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                phone="invalid",  # Invalid phone
                date_of_birth=date(1990, 1, 1),
                gender="M",
                address="Test St",
                employee_id="EMP100",
                department=department,
                hire_date=date(2020, 1, 1),
                status="ACTIVE",
                base_salary=Decimal("50000.00")
            )
            emp.full_clean()

    def test_employee_full_name_property(self, employee):
        """Test full_name property."""
        assert employee.full_name == "John Doe"

    def test_employee_years_of_service(self, db, department):
        """Test years_of_service property."""
        emp = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+1234567890",
            date_of_birth=date(1990, 1, 15),
            gender="M",
            address="123 Main St",
            employee_id="EMP001",
            department=department,
            position="Developer",
            hire_date=date(2020, 1, 1),
            status="ACTIVE",
            base_salary=Decimal("50000.00")
        )
        # Approximate calculation
        years = emp.years_of_service
        assert isinstance(years, int)
        assert years >= 0

    def test_employee_gender_choices(self, db, department):
        """Test gender choices."""
        for gender_code, gender_name in Employee.GENDER_CHOICES:
            emp = Employee.objects.create(
                first_name=f"Test{gender_code}",
                last_name="User",
                email=f"test{gender_code}@example.com",
                phone=f"+123456789{gender_code}",
                date_of_birth=date(1990, 1, 1),
                gender=gender_code,
                address="Test St",
                employee_id=f"EMP{gender_code}",
                department=department,
                hire_date=date(2020, 1, 1),
                status="ACTIVE",
                base_salary=Decimal("50000.00")
            )
            assert emp.gender == gender_code

    def test_employee_status_choices(self, db, department):
        """Test employment status choices."""
        statuses = ['ACTIVE', 'INACTIVE', 'SUSPENDED', 'ON_LEAVE']
        for idx, status in enumerate(statuses):
            emp = Employee.objects.create(
                first_name=f"Test{idx}",
                last_name="User",
                email=f"test{idx}@example.com",
                phone=f"+1234567890{idx}",
                date_of_birth=date(1990, 1, 1),
                gender="M",
                address="Test St",
                employee_id=f"EMP{idx:03d}",
                department=department,
                hire_date=date(2020, 1, 1),
                status=status,
                base_salary=Decimal("50000.00")
            )
            assert emp.status == status

    def test_employee_str_representation(self, employee):
        """Test employee string representation."""
        assert str(employee) == "John Doe (EMP001)"

    def test_employee_ordering(self, db, department):
        """Test that employees are ordered by employee_id."""
        Employee.objects.create(
            first_name="Zoe", last_name="Last",
            email="zoe@example.com", phone="+1234567890",
            date_of_birth=date(1990, 1, 1), gender="F",
            address="Test", employee_id="EMP003",
            department=department, hire_date=date(2020, 1, 1),
            status="ACTIVE", base_salary=Decimal("50000.00")
        )
        Employee.objects.create(
            first_name="Alice", last_name="First",
            email="alice@example.com", phone="+0987654321",
            date_of_birth=date(1991, 2, 2), gender="F",
            address="Test", employee_id="EMP001",
            department=department, hire_date=date(2020, 1, 1),
            status="ACTIVE", base_salary=Decimal("50000.00")
        )

        emps = list(Employee.objects.all())
        assert emps[0].employee_id == "EMP001"

    def test_employee_department_relationship(self, employee, department):
        """Test employee-department relationship."""
        assert employee.department == department

    def test_employee_department_set_null_on_delete(self, db, department, employee):
        """Test that employee department is set to NULL when department is deleted."""
        department.delete()
        employee.refresh_from_db()
        assert employee.department is None

    def test_employee_salary_fields(self, employee):
        """Test salary and allowance fields."""
        assert employee.base_salary == Decimal("50000.00")
        assert employee.allowance == Decimal("5000.00")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LEAVE MODEL TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestLeaveModel:
    """Test cases for Leave model."""

    def test_leave_creation(self, db, employee):
        """Test creating a leave request."""
        leave = Leave.objects.create(
            employee=employee,
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 5),
            reason="Annual vacation",
            status="PENDING"
        )
        assert leave.id is not None
        assert leave.employee == employee
        assert leave.status == "PENDING"

    def test_leave_status_choices(self, db, employee):
        """Test leave status choices."""
        statuses = ['PENDING', 'APPROVED', 'REJECTED', 'CANCELLED']
        for status in statuses:
            leave = Leave.objects.create(
                employee=employee,
                start_date=date(2024, 6, 1),
                end_date=date(2024, 6, 5),
                reason=f"Leave - {status}",
                status=status
            )
            assert leave.status == status

    def test_leave_validation_start_before_end(self, db, employee):
        """Test that start_date must be before end_date."""
        leave = Leave(
            employee=employee,
            start_date=date(2024, 6, 10),
            end_date=date(2024, 6, 5),  # End before start
            reason="Invalid dates"
        )
        with pytest.raises(ValidationError):
            leave.full_clean()

    def test_leave_duration_days_property(self, employee):
        """Test duration_days property calculation."""
        leave = Leave.objects.create(
            employee=employee,
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 5),
            reason="5 day vacation"
        )
        assert leave.duration_days == 5

    def test_leave_single_day_duration(self, employee):
        """Test duration for single day leave."""
        leave = Leave.objects.create(
            employee=employee,
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 1),
            reason="Single day"
        )
        assert leave.duration_days == 1

    def test_leave_str_representation(self, leave_approved):
        """Test leave string representation."""
        expected = f"{leave_approved.employee.full_name} ({leave_approved.start_date} to {leave_approved.end_date})"
        assert str(leave_approved) == expected

    def test_leave_employee_relationship(self, employee, leave_pending):
        """Test leave-employee relationship."""
        assert leave_pending.employee == employee
        assert leave_pending in employee.leaves.all()

    def test_leave_approved_by_relationship(self, leave_approved, employee2):
        """Test approved_by relationship."""
        assert leave_approved.approved_by == employee2

    def test_leave_ordering(self, db, employee):
        """Test that leaves are ordered by start_date descending."""
        Leave.objects.create(
            employee=employee,
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 5),
            reason="Earlier leave"
        )
        Leave.objects.create(
            employee=employee,
            start_date=date(2024, 7, 1),
            end_date=date(2024, 7, 5),
            reason="Later leave"
        )

        leaves = list(Leave.objects.all())
        assert leaves[0].start_date > leaves[1].start_date


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ATTENDANCE MODEL TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestAttendanceModel:
    """Test cases for Attendance model."""

    def test_attendance_creation(self, db, employee):
        """Test creating an attendance record."""
        att = Attendance.objects.create(
            employee=employee,
            date=date.today(),
            check_in_time=time(9, 0),
            check_out_time=time(17, 0),
            status="PRESENT"
        )
        assert att.id is not None
        assert att.employee == employee
        assert att.status == "PRESENT"

    def test_attendance_status_choices(self, db, employee):
        """Test attendance status choices."""
        statuses = ['PRESENT', 'ABSENT', 'LATE',
                    'EARLY_LEAVE', 'HALF_DAY', 'ON_LEAVE']
        for idx, status in enumerate(statuses):
            date_val = date.today() - timedelta(days=idx)
            att = Attendance.objects.create(
                employee=employee,
                date=date_val,
                status=status
            )
            assert att.status == status

    def test_attendance_working_hours_calculation(self, db, employee):
        """Test working_hours property calculation."""
        att = Attendance.objects.create(
            employee=employee,
            date=date.today(),
            check_in_time=time(9, 0),
            check_out_time=time(17, 0),
            status="PRESENT"
        )
        assert att.working_hours == 8.0

    def test_attendance_working_hours_with_minutes(self, db, employee):
        """Test working hours calculation with minutes."""
        att = Attendance.objects.create(
            employee=employee,
            date=date.today(),
            check_in_time=time(9, 30),
            check_out_time=time(17, 45),
            status="PRESENT"
        )
        expected = 8.25  # 8 hours 15 minutes
        assert att.working_hours == expected

    def test_attendance_working_hours_none_without_times(self, db, employee):
        """Test working_hours is None when check times are missing."""
        att = Attendance.objects.create(
            employee=employee,
            date=date.today(),
            status="ABSENT"
        )
        assert att.working_hours is None

    def test_attendance_unique_together(self, db, employee):
        """Test unique_together constraint for employee and date."""
        Attendance.objects.create(
            employee=employee,
            date=date.today(),
            status="PRESENT"
        )

        with pytest.raises(IntegrityError):
            Attendance.objects.create(
                employee=employee,
                date=date.today(),  # Same employee and date
                status="ABSENT"
            )

    def test_attendance_str_representation(self, attendance_present):
        """Test attendance string representation."""
        expected = f"{attendance_present.employee.full_name} - {attendance_present.date} ({attendance_present.status})"
        assert str(attendance_present) == expected

    def test_attendance_ordering(self, db, employee):
        """Test that attendances are ordered by date descending."""
        Attendance.objects.create(
            employee=employee,
            date=date.today() - timedelta(days=5),
            status="PRESENT"
        )
        Attendance.objects.create(
            employee=employee,
            date=date.today(),
            status="PRESENT"
        )

        attendances = list(Attendance.objects.all())
        assert attendances[0].date > attendances[1].date

    def test_attendance_employee_relationship(self, employee, attendance_present):
        """Test attendance-employee relationship."""
        assert attendance_present.employee == employee
        assert attendance_present in employee.attendances.all()

    def test_attendance_half_day_status(self, db, employee):
        """Test half-day attendance."""
        att = Attendance.objects.create(
            employee=employee,
            date=date.today(),
            check_in_time=time(9, 0),
            check_out_time=time(13, 0),
            status="HALF_DAY"
        )
        assert att.status == "HALF_DAY"
        assert att.working_hours == 4.0

    def test_attendance_optional_notes(self, db, employee):
        """Test that notes field is optional."""
        att = Attendance.objects.create(
            employee=employee,
            date=date.today(),
            status="PRESENT"
        )
        assert att.notes is None

    def test_attendance_with_notes(self, db, employee):
        """Test attendance with notes."""
        note = "Left early for doctor's appointment"
        att = Attendance.objects.create(
            employee=employee,
            date=date.today(),
            check_in_time=time(9, 0),
            check_out_time=time(14, 0),
            status="EARLY_LEAVE",
            notes=note
        )
        assert att.notes == note
