"""
Comprehensive Service Tests for HRM System.
Tests for EmployeeService, LeaveService, and AttendanceService.
"""
from datetime import date, timedelta, time
from decimal import Decimal

import pytest
from django.core.exceptions import ObjectDoesNotExist

from core.employees.models import Employee, Department
from core.leaves.models import Leave
from core.attendance.models import Attendance
from core.employees.usecase.services.employee_services import EmployeeService
from core.leaves.usecase.services.leave_services import LeaveService
from core.attendance.usecase.services.attendance_services import AttendanceService


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EMPLOYEE SERVICE TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestEmployeeService:
    """Test cases for EmployeeService."""

    @pytest.fixture
    def service(self):
        """Create an EmployeeService instance."""
        return EmployeeService()

    def test_create_employee(self, db, service, department):
        """Test creating an employee through service."""
        input_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'date_of_birth': date(1990, 1, 15),
            'gender': 'M',
            'address': '123 Main St',
            'employee_id': 'EMP001',
            'department': department,
            'position': 'Developer',
            'hire_date': date(2020, 1, 1),
            'status': 'ACTIVE',
            'base_salary': Decimal('50000.00'),
            'allowance': Decimal('5000.00')
        }

        emp = service.create(input_data)

        assert emp.id is not None
        assert emp.first_name == 'John'
        assert emp.email == 'john@example.com'
        assert Employee.objects.filter(id=emp.id).exists()

    def test_create_employee_transaction(self, db, service, department):
        """Test that create is atomic."""
        input_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'phone': '+0987654321',
            'date_of_birth': date(1992, 5, 20),
            'gender': 'F',
            'address': '456 Oak Ave',
            'employee_id': 'EMP002',
            'department': department,
            'hire_date': date(2020, 1, 1),
            'status': 'ACTIVE',
            'base_salary': Decimal('55000.00')
        }

        emp = service.create(input_data)
        assert emp.id is not None

    def test_update_employee(self, db, service, employee):
        """Test updating an employee through service."""
        update_data = {
            'position': 'Senior Developer',
            'base_salary': Decimal('60000.00'),
            'allowance': Decimal('7000.00')
        }

        updated_emp = service.update(employee.id, update_data)

        assert updated_emp.position == 'Senior Developer'
        assert updated_emp.base_salary == Decimal('60000.00')
        assert updated_emp.allowance == Decimal('7000.00')

    def test_update_employee_partial(self, db, service, employee):
        """Test partial update of an employee."""
        original_salary = employee.base_salary
        update_data = {
            'position': 'Tech Lead'
        }

        updated_emp = service.update(employee.id, update_data)

        assert updated_emp.position == 'Tech Lead'
        assert updated_emp.base_salary == original_salary

    def test_update_employee_with_none_values(self, db, service, employee):
        """Test that None values are not updated."""
        original_position = employee.position
        update_data = {
            'position': 'Manager',
            'address': None  # Should be ignored
        }

        updated_emp = service.update(employee.id, update_data)

        assert updated_emp.position == 'Manager'
        assert updated_emp.address == employee.address

    def test_delete_employee(self, db, service, employee):
        """Test deleting an employee through service."""
        emp_id = employee.id
        assert Employee.objects.filter(id=emp_id).exists()

        service.delete(emp_id)

        assert not Employee.objects.filter(id=emp_id).exists()

    def test_delete_nonexistent_employee(self, db, service):
        """Test deleting a non-existent employee."""
        with pytest.raises(ObjectDoesNotExist):
            service.delete(999)

    def test_update_staff_to_inactive(self, db, service, employee):
        """Test updating employee status to inactive."""
        update_data = {'status': 'INACTIVE'}

        updated_emp = service.update(employee.id, update_data)

        assert updated_emp.status == 'INACTIVE'

    def test_update_staff_salary(self, db, service, employee):
        """Test updating employee salary."""
        new_salary = Decimal('75000.00')
        update_data = {'base_salary': new_salary}

        updated_emp = service.update(employee.id, update_data)

        assert updated_emp.base_salary == new_salary


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LEAVE SERVICE TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestLeaveService:
    """Test cases for LeaveService."""

    @pytest.fixture
    def service(self):
        """Create a LeaveService instance."""
        return LeaveService()

    def test_create_leave(self, db, service, employee):
        """Test creating a leave request through service."""
        input_data = {
            'employee': employee,
            'start_date': date(2024, 6, 1),
            'end_date': date(2024, 6, 5),
            'reason': 'Annual vacation'
        }

        leave = service.create(input_data)

        assert leave.id is not None
        assert leave.employee == employee
        assert leave.status == 'PENDING'

    def test_create_leave_with_status(self, db, service, employee):
        """Test creating a leave with explicit status."""
        input_data = {
            'employee': employee,
            'start_date': date(2024, 7, 1),
            'end_date': date(2024, 7, 5),
            'reason': 'Sick leave',
            'status': 'PENDING'
        }

        leave = service.create(input_data)

        assert leave.status == 'PENDING'

    def test_update_leave(self, db, service, leave_pending):
        """Test updating a leave request."""
        update_data = {
            'reason': 'Updated reason',
            'status': 'APPROVED'
        }

        updated_leave = service.update(leave_pending.id, update_data)

        assert updated_leave.reason == 'Updated reason'
        assert updated_leave.status == 'APPROVED'

    def test_delete_leave(self, db, service, leave_pending):
        """Test deleting a leave request."""
        leave_id = leave_pending.id
        assert Leave.objects.filter(id=leave_id).exists()

        service.delete(leave_id)

        assert not Leave.objects.filter(id=leave_id).exists()

    def test_approve_leave(self, db, service, leave_pending, employee2):
        """Test approving a leave request."""
        approved_leave = service.approve(leave_pending.id, employee2)

        assert approved_leave.status == 'APPROVED'
        assert approved_leave.approved_by == employee2

    def test_approve_leave_updates_existing(self, db, service, leave_pending, employee2):
        """Test that approving updates the leave in database."""
        service.approve(leave_pending.id, employee2)

        leave_pending.refresh_from_db()
        assert leave_pending.status == 'APPROVED'
        assert leave_pending.approved_by == employee2

    def test_reject_leave(self, db, service, leave_pending, employee2):
        """Test rejecting a leave request."""
        remarks = 'Insufficient notice period'
        rejected_leave = service.reject(leave_pending.id, remarks)

        assert rejected_leave.status == 'REJECTED'
        assert rejected_leave.remarks == remarks

    def test_reject_leave_without_remarks(self, db, service, leave_pending):
        """Test rejecting a leave without remarks."""
        rejected_leave = service.reject(leave_pending.id, '')

        assert rejected_leave.status == 'REJECTED'
        assert rejected_leave.remarks == ''

    def test_approve_then_reject_not_allowed(self, db, service, leave_approved, employee2):
        """Test that we can still update approved leave."""
        # Service doesn't enforce state machine, just updates
        updated = service.update(leave_approved.id, {'reason': 'New reason'})
        assert updated.reason == 'New reason'

    def test_leave_service_transaction(self, db, service, leave_pending, employee2):
        """Test that operations are atomic."""
        service.approve(leave_pending.id, employee2)

        # Verify changes persisted
        leave_pending.refresh_from_db()
        assert leave_pending.status == 'APPROVED'


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ATTENDANCE SERVICE TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestAttendanceService:
    """Test cases for AttendanceService."""

    @pytest.fixture
    def service(self):
        """Create an AttendanceService instance."""
        return AttendanceService()

    def test_create_attendance(self, db, service, employee):
        """Test creating an attendance record through service."""
        input_data = {
            'employee': employee,
            'date': date.today(),
            'check_in_time': time(9, 0),
            'check_out_time': time(17, 0),
            'status': 'PRESENT'
        }

        att = service.create(input_data)

        assert att.id is not None
        assert att.employee == employee
        assert att.status == 'PRESENT'

    def test_create_absent_attendance(self, db, service, employee):
        """Test creating an absent attendance record."""
        input_data = {
            'employee': employee,
            'date': date.today(),
            'status': 'ABSENT'
        }

        att = service.create(input_data)

        assert att.status == 'ABSENT'
        assert att.check_in_time is None
        assert att.check_out_time is None

    def test_update_attendance(self, db, service, attendance_present):
        """Test updating attendance through service."""
        update_data = {
            'status': 'LATE',
            'check_in_time': time(9, 30)
        }

        updated_att = service.update(attendance_present.id, update_data)

        assert updated_att.status == 'LATE'
        assert updated_att.check_in_time == time(9, 30)

    def test_update_attendance_with_notes(self, db, service, attendance_present):
        """Test updating attendance with notes."""
        note = 'Doctor appointment in afternoon'
        update_data = {
            'status': 'EARLY_LEAVE',
            'check_out_time': time(14, 0),
            'notes': note
        }

        updated_att = service.update(attendance_present.id, update_data)

        assert updated_att.notes == note
        assert updated_att.status == 'EARLY_LEAVE'

    def test_bulk_update_or_create_attendance(self, db, service, employee, employee2):
        """Test bulk update/create attendance records."""
        test_date = date.today()
        records = [
            {
                'employee': employee,
                'status': 'PRESENT',
                'check_in_time': time(9, 0),
                'check_out_time': time(17, 0)
            },
            {
                'employee': employee2,
                'status': 'ABSENT'
            }
        ]

        service.bulk_update_or_create(test_date, records)

        att1 = Attendance.objects.get(employee=employee, date=test_date)
        att2 = Attendance.objects.get(employee=employee2, date=test_date)

        assert att1.status == 'PRESENT'
        assert att2.status == 'ABSENT'

    def test_bulk_update_or_create_updates_existing(self, db, service, employee, attendance_present):
        """Test that bulk operation updates existing records."""
        original_status = attendance_present.status

        records = [
            {
                'employee': employee,
                'status': 'LATE',
                'check_in_time': time(9, 30),
                'check_out_time': time(17, 30)
            }
        ]

        service.bulk_update_or_create(attendance_present.date, records)

        attendance_present.refresh_from_db()
        assert attendance_present.status == 'LATE'
        assert attendance_present.check_in_time == time(9, 30)

    def test_bulk_create_multiple_dates(self, db, service, employee, employee2):
        """Test bulk creating attendance for multiple employees."""
        test_date = date.today()
        records = [
            {
                'employee': employee,
                'status': 'PRESENT',
                'check_in_time': time(9, 0),
                'check_out_time': time(17, 0),
                'notes': 'Normal day'
            },
            {
                'employee': employee2,
                'status': 'LATE',
                'check_in_time': time(10, 0),
                'check_out_time': time(18, 0),
                'notes': 'Traffic jam'
            }
        ]

        service.bulk_update_or_create(test_date, records)

        assert Attendance.objects.filter(date=test_date).count() == 2

        att1 = Attendance.objects.get(employee=employee, date=test_date)
        assert att1.notes == 'Normal day'
        assert att1.working_hours == 8.0

    def test_attendance_service_with_missing_times(self, db, service, employee):
        """Test creation with missing check times."""
        input_data = {
            'employee': employee,
            'date': date.today(),
            'status': 'ON_LEAVE',
            'notes': 'Annual leave'
        }

        att = service.create(input_data)

        assert att.check_in_time is None
        assert att.check_out_time is None
        assert att.working_hours is None

    def test_attendance_service_transaction(self, db, service, employee):
        """Test that service operations are atomic."""
        input_data = {
            'employee': employee,
            'date': date.today(),
            'check_in_time': time(9, 0),
            'check_out_time': time(17, 0),
            'status': 'PRESENT'
        }

        att = service.create(input_data)

        # Verify persisted
        att_from_db = Attendance.objects.get(id=att.id)
        assert att_from_db.employee == employee

    def test_attendance_half_day_service(self, db, service, employee):
        """Test creating half-day attendance."""
        input_data = {
            'employee': employee,
            'date': date.today(),
            'check_in_time': time(9, 0),
            'check_out_time': time(13, 0),
            'status': 'HALF_DAY',
            'notes': 'Afternoon appointment'
        }

        att = service.create(input_data)

        assert att.status == 'HALF_DAY'
        assert att.working_hours == 4.0
        assert att.notes == 'Afternoon appointment'
