from core.employees.models import Employee
from django.db import transaction
from dataclasses import dataclass


@dataclass
class EmployeeService:
    @transaction.atomic
    def create(self, input: dict):
        employee = Employee.objects.create(**input)
        return employee

    @transaction.atomic
    def update(self, pk, input: dict):
        employee = Employee.objects.get(pk=pk)
        for key, value in input.items():
            if hasattr(employee, key) and value is not None:
                setattr(employee, key, value)
        employee.save()
        return employee

    @transaction.atomic
    def delete(self, pk):
        employee = Employee.objects.get(pk=pk)
        employee.delete()
