from core.employees.models import Employee, Department, Position
from django.db.models import Q


def get_all_employees():
    """Get all employees"""
    return Employee.objects.select_related('department', 'position').all()


def get_employee_by_id(employee_id):
    """Get employee by ID"""
    return Employee.objects.select_related('department', 'position', 'attendances', 'leaves').get(id=employee_id)


def search_employees(search_term):
    """Search employees by name, email, or ID"""
    return Employee.objects.filter(
        Q(first_name__icontains=search_term) |
        Q(last_name__icontains=search_term) |
        Q(email__icontains=search_term) |
        Q(employee_id__icontains=search_term)
    ).select_related('department', 'position')


def get_employees_by_department(department_id):
    """Get employees by department"""
    return Employee.objects.filter(department_id=department_id).select_related('position')


def get_employees_by_status(status):
    """Get employees by status"""
    return Employee.objects.filter(status=status).select_related('department', 'position')


def get_active_employees():
    """Get active employees"""
    return get_employees_by_status('ACTIVE')
