from core.employees.models import Employee, Department
from django.db.models import Q
from django.shortcuts import get_object_or_404


class EmployeeSelector:
    def list(self, filters=None):
        filters = filters or {}
        queryset = Employee.objects.select_related('department')

        search = filters.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(employee_id__icontains=search) |
                Q(email__icontains=search)
            )

        department = filters.get('department', '')
        if department:
            queryset = queryset.filter(department_id=department)

        status = filters.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_by_id(self, pk):
        return get_object_or_404(
            Employee.objects.select_related('department'),
            pk=pk
        )

    def get_active(self):
        return Employee.objects.filter(status='ACTIVE')


class DepartmentSelector:
    def list(self):
        return Department.objects.all()

    def get_by_id(self, pk):
        return get_object_or_404(Department, pk=pk)
