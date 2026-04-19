"""
Comprehensive Selector Tests for HRM System.
Tests for EmployeeSelector, DepartmentSelector, LeaveSelector, and AttendanceSelector.
"""
from datetime import date, timedelta, time
from decimal import Decimal

import pytest
from django.http import Http404

from core.employees.models import Employee, Department
from core.leaves.models import Leave
from core.attendance.models import Attendance
from core.employees.usecase.selectors.employee_selectors import (
    EmployeeSelector, DepartmentSelector
)
from core.leaves.usecase.selectors.leave_selectors import LeaveSelector
from core.attendance.usecase.selectors.attendance_selectors import AttendanceSelector


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EMPLOYEE SELECTOR TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestEmployeeSelector:
    """Test cases for EmployeeSelector."""

    @pytest.fixture
    def selector(self):
        """Create an EmployeeSelector instance."""
        return EmployeeSelector()

    def test_list_all_employees(self, db, selector, employees):
        """Test listing all employees."""
        emp_list = selector.list()

        assert emp_list.count() == 2
        assert emp_list[0] in employees
        assert emp_list[1] in employees

    def test_list_with_empty_filters(self, db, selector, employees):
        """Test listing with empty filter dict."""
        emp_list = selector.list(filters={})

        assert emp_list.count() == 2

    def test_list_with_none_filters(self, db, selector, employees):
        """Test listing with None filters."""
        emp_list = selector.list(filters=None)

        assert emp_list.count() == 2

    def test_search_by_first_name(self, db, selector, employee, employee2):
        """Test searching employees by first name."""
        emp_list = selector.list(filters={'search': 'John'})

        assert emp_list.count() == 1
        assert emp_list[0] == employee

    def test_search_by_last_name(self, db, selector, employee, employee2):
        """Test searching employees by last name."""
        emp_list = selector.list(filters={'search': 'Smith'})

        assert emp_list.count() == 1
        assert emp_list[0] == employee2

    def test_search_by_employee_id(self, db, selector, employee):
        """Test searching employees by employee ID."""
        emp_list = selector.list(filters={'search': 'EMP001'})

        assert emp_list.count() == 1
        assert emp_list[0] == employee

    def test_search_by_email(self, db, selector, employee):
        """Test searching employees by email."""
        emp_list = selector.list(filters={'search': 'john.doe@example.com'})

        assert emp_list.count() == 1
        assert emp_list[0] == employee

    def test_search_case_insensitive(self, db, selector, employee):
        """Test that search is case insensitive."""
        emp_list = selector.list(filters={'search': 'JOHN'})

        assert emp_list.count() == 1
        assert emp_list[0] == employee

    def test_search_partial_match(self, db, selector, employee, employee2):
        """Test partial search matches."""
        emp_list = selector.list(filters={'search': 'Smith'})

        assert emp_list.count() == 1

    def test_search_no_matches(self, db, selector):
        """Test search with no matches."""
        emp_list = selector.list(filters={'search': 'NonExistent'})

        assert emp_list.count() == 0

    def test_filter_by_department(self, db, selector, employee, employee2, hr_department):
        """Test filtering by department."""
        hr_emp = Employee.objects.create(
            first_name="HR",
            last_name="Manager",
            email="hr@example.com",
            phone="+5555555555",
            date_of_birth=date(1988, 1, 1),
            gender="M",
            address="Test",
            employee_id="EMP004",
            department=hr_department,
            hire_date=date(2019, 1, 1),
            status="ACTIVE",
            base_salary=Decimal("45000.00")
        )

        emp_list = selector.list(filters={'department': hr_department.id})

        assert emp_list.count() == 1
        assert emp_list[0] == hr_emp

    def test_filter_by_status(self, db, selector, employee, inactive_employee):
        """Test filtering by employment status."""
        emp_list = selector.list(filters={'status': 'ACTIVE'})

        assert emp_list.count() >= 1
        assert all(e.status == 'ACTIVE' for e in emp_list)

    def test_filter_active_employees(self, db, selector, employees, inactive_employee):
        """Test filtering active employees."""
        emp_list = selector.list(filters={'status': 'ACTIVE'})

        assert inactive_employee not in emp_list
        assert all(e.status == 'ACTIVE' for e in emp_list)

    def test_combined_filters(self, db, selector, employee, employee2, department):
        """Test combining search and status filters."""
        emp_list = selector.list(filters={
            'search': 'John',
            'status': 'ACTIVE',
            'department': department.id
        })

        assert emp_list.count() == 1
        assert emp_list[0] == employee

    def test_get_by_id(self, db, selector, employee):
        """Test getting employee by ID."""
        emp = selector.get_by_id(employee.id)

        assert emp == employee
        assert emp.first_name == 'John'

    def test_get_by_id_nonexistent(self, db, selector):
        """Test getting non-existent employee."""
        with pytest.raises(Http404):
            selector.get_by_id(999)

    def test_get_by_id_with_department(self, db, selector, employee):
        """Test that get_by_id includes department."""
        emp = selector.get_by_id(employee.id)

        assert emp.department == employee.department

    def test_get_active_employees(self, db, selector, employees, inactive_employee):
        """Test getting only active employees."""
        active = selector.get_active()

        assert inactive_employee not in list(active)
        assert all(e.status == 'ACTIVE' for e in active)

    def test_get_active_empty(self, db, selector, inactive_employee):
        """Test get_active when no active employees."""
        # Deactivate all active employees
        for emp in Employee.objects.filter(status='ACTIVE'):
            emp.status = 'INACTIVE'
            emp.save()

        active = selector.get_active()

        assert active.count() == 0

    def test_selector_uses_select_related(self, db, selector, employee):
        """Test that selector optimizes queries with select_related."""
        emp_list = selector.list()

        # Should have pre-fetched department to avoid additional queries
        emp = emp_list[0]
        assert emp.department is not None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DEPARTMENT SELECTOR TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestDepartmentSelector:
    """Test cases for DepartmentSelector."""

    @pytest.fixture
    def selector(self):
        """Create a DepartmentSelector instance."""
        return DepartmentSelector()

    def test_list_all_departments(self, db, selector, departments):
        """Test listing all departments."""
        dept_list = selector.list()

        assert dept_list.count() == 2

    def test_list_departments_empty(self, db, selector):
        """Test listing departments when none exist."""
        dept_list = selector.list()

        assert dept_list.count() == 0

    def test_get_department_by_id(self, db, selector, department):
        """Test getting department by ID."""
        dept = selector.get_by_id(department.id)

        assert dept == department
        assert dept.name == 'Engineering'

    def test_get_department_by_id_nonexistent(self, db, selector):
        """Test getting non-existent department."""
        with pytest.raises(Http404):
            selector.get_by_id(999)

    def test_departments_ordered_by_name(self, db, selector):
        """Test that departments are ordered by name."""
        Department.objects.create(name="Zebra")
        Department.objects.create(name="Alpha")
        Department.objects.create(name="Beta")

        depts = list(selector.list())
        names = [d.name for d in depts]

        assert names == ['Alpha', 'Beta', 'Zebra']


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LEAVE SELECTOR TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestLeaveSelector:
    """Test cases for LeaveSelector."""

    @pytest.fixture
    def selector(self):
        """Create a LeaveSelector instance."""
        return LeaveSelector()

    def test_list_all_leaves(self, db, selector, leaves):
        """Test listing all leaves."""
        leave_list = selector.list()

        assert leave_list.count() == 3

    def test_list_with_empty_filters(self, db, selector, leaves):
        """Test listing with empty filters."""
        leave_list = selector.list(filters={})

        assert leave_list.count() == 3

    def test_list_with_none_filters(self, db, selector, leaves):
        """Test listing with None filters."""
        leave_list = selector.list(filters=None)

        assert leave_list.count() == 3

    def test_search_by_employee_first_name(self, db, selector, leave_pending, employee):
        """Test searching leaves by employee first name."""
        leave_list = selector.list(filters={'search': employee.first_name})

        assert leave_list.count() >= 1
        assert leave_pending in leave_list

    def test_search_by_employee_last_name(self, db, selector, leave_pending, employee):
        """Test searching leaves by employee last name."""
        leave_list = selector.list(filters={'search': employee.last_name})

        assert leave_list.count() >= 1
        assert leave_pending in leave_list

    def test_search_case_insensitive(self, db, selector, leave_pending, employee):
        """Test case insensitive search."""
        leave_list = selector.list(
            filters={'search': employee.first_name.upper()})

        assert leave_pending in leave_list

    def test_filter_by_status_pending(self, db, selector, leaves):
        """Test filtering by PENDING status."""
        leave_list = selector.list(filters={'status': 'PENDING'})

        assert leave_list.count() >= 1
        assert all(l.status == 'PENDING' for l in leave_list)

    def test_filter_by_status_approved(self, db, selector, leaves):
        """Test filtering by APPROVED status."""
        leave_list = selector.list(filters={'status': 'APPROVED'})

        assert leave_list.count() >= 1
        assert all(l.status == 'APPROVED' for l in leave_list)

    def test_filter_by_status_rejected(self, db, selector, leaves):
        """Test filtering by REJECTED status."""
        leave_list = selector.list(filters={'status': 'REJECTED'})

        assert leave_list.count() >= 1
        assert all(l.status == 'REJECTED' for l in leave_list)

    def test_filter_by_status_cancelled(self, db, selector, employee):
        """Test filtering by CANCELLED status."""
        Leave.objects.create(
            employee=employee,
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=35),
            reason="Cancelled leave",
            status="CANCELLED"
        )

        leave_list = selector.list(filters={'status': 'CANCELLED'})

        assert leave_list.count() >= 1

    def test_combined_filters(self, db, selector, leave_approved, employee):
        """Test combining search and status filters."""
        leave_list = selector.list(filters={
            'search': employee.first_name,
            'status': 'APPROVED'
        })

        assert leave_approved in leave_list

    def test_list_ordering(self, db, selector, employee):
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

        leave_list = list(selector.list())

        # More recent first
        assert leave_list[0].start_date >= leave_list[1].start_date

    def test_get_by_id(self, db, selector, leave_pending):
        """Test getting leave by ID."""
        leave = selector.get_by_id(leave_pending.id)

        assert leave == leave_pending

    def test_get_by_id_nonexistent(self, db, selector):
        """Test getting non-existent leave."""
        with pytest.raises(Http404):
            selector.get_by_id(999)

    def test_get_by_id_with_relations(self, db, selector, leave_approved):
        """Test that get_by_id includes relationships."""
        leave = selector.get_by_id(leave_approved.id)

        assert leave.employee is not None
        assert leave.approved_by is not None

    def test_selector_optimization(self, db, selector, leave_approved):
        """Test that selector optimizes queries."""
        leave = selector.get_by_id(leave_approved.id)

        # Should have pre-fetched employee and approved_by
        assert leave.employee is not None
        assert leave.approved_by is not None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ATTENDANCE SELECTOR TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestAttendanceSelector:
    """Test cases for AttendanceSelector."""

    @pytest.fixture
    def selector(self):
        """Create an AttendanceSelector instance."""
        return AttendanceSelector()

    def test_list_all_attendance(self, db, selector, attendances):
        """Test listing all attendance records."""
        att_list = selector.list()

        assert att_list.count() == 4

    def test_list_with_empty_filters(self, db, selector, attendances):
        """Test listing with empty filters."""
        att_list = selector.list(filters={})

        assert att_list.count() == 4

    def test_list_with_none_filters(self, db, selector, attendances):
        """Test listing with None filters."""
        att_list = selector.list(filters=None)

        assert att_list.count() == 4

    def test_filter_by_employee(self, db, selector, employee, attendances):
        """Test filtering by employee."""
        att_list = selector.list(filters={'employee': employee.id})

        # attendances fixture has employee in multiple records
        assert all(a.employee == employee for a in att_list)

    def test_filter_by_status_present(self, db, selector, attendances):
        """Test filtering by PRESENT status."""
        att_list = selector.list(filters={'status': 'PRESENT'})

        assert all(a.status == 'PRESENT' for a in att_list)

    def test_filter_by_status_absent(self, db, selector, attendances):
        """Test filtering by ABSENT status."""
        att_list = selector.list(filters={'status': 'ABSENT'})

        assert all(a.status == 'ABSENT' for a in att_list)

    def test_filter_by_date_range(self, db, selector, employee):
        """Test filtering by date range."""
        today = date.today()
        past_date = today - timedelta(days=10)
        future_date = today + timedelta(days=10)

        # Create attendance on past date
        Attendance.objects.create(
            employee=employee,
            date=past_date,
            status='PRESENT'
        )

        att_list = selector.list(filters={
            'from_date': past_date,
            'to_date': today
        })

        assert all(a.date >= past_date and a.date <= today for a in att_list)

    def test_filter_from_date_only(self, db, selector, employee):
        """Test filtering with only from_date."""
        today = date.today()
        past_date = today - timedelta(days=10)

        Attendance.objects.create(
            employee=employee,
            date=past_date,
            status='PRESENT'
        )

        att_list = selector.list(filters={'from_date': past_date})

        assert all(a.date >= past_date for a in att_list)

    def test_filter_to_date_only(self, db, selector, employee):
        """Test filtering with only to_date."""
        today = date.today()
        future_date = today + timedelta(days=10)

        att_list = selector.list(filters={'to_date': today})

        assert all(a.date <= today for a in att_list)

    def test_combined_filters(self, db, selector, employee):
        """Test combining multiple filters."""
        today = date.today()

        att_list = selector.list(filters={
            'employee': employee.id,
            'status': 'PRESENT',
            'from_date': today - timedelta(days=5),
            'to_date': today
        })

        assert all(a.employee == employee for a in att_list)
        assert all(a.status == 'PRESENT' for a in att_list)

    def test_list_ordering(self, db, selector, attendances):
        """Test that attendance is ordered by date descending."""
        att_list = list(selector.list())

        # Most recent first
        for i in range(len(att_list) - 1):
            assert att_list[i].date >= att_list[i + 1].date

    def test_get_by_id(self, db, selector, attendance_present):
        """Test getting attendance by ID."""
        att = selector.get_by_id(attendance_present.id)

        assert att == attendance_present

    def test_get_by_id_nonexistent(self, db, selector):
        """Test getting non-existent attendance."""
        with pytest.raises(Http404):
            selector.get_by_id(999)


    def test_get_by_date(self, db, selector, employee):
        """Test getting attendance records by date."""
        today = date.today()
        att = Attendance.objects.create(
            employee=employee,
            date=today,
            status='PRESENT'
        )

        att_list = selector.get_by_date(today)

        assert att in att_list

    def test_get_by_date_empty(self, db, selector):
        """Test getting attendance for date with no records."""
        future_date = date.today() + timedelta(days=100)

        att_list = selector.get_by_date(future_date)

        assert att_list.count() == 0

    def test_selector_optimization(self, db, selector, employee):
        """Test selector query optimization."""
        Attendance.objects.create(
            employee=employee,
            date=date.today(),
            status='PRESENT'
        )

        att_list = selector.list()

        # Should have pre-fetched employee
        if att_list.exists():
            att = att_list[0]
            assert att.employee is not None
