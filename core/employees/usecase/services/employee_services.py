from core.employees.models import Employee
from django.db import transaction
from django.contrib.auth.models import User
from dataclasses import dataclass


@dataclass
class EmployeeService:
    @transaction.atomic
    def create(self, input: dict):
        # Extract username and password from input
        username = input.pop('username', None)
        password = input.pop('password', None)

        # Create User account if username and password provided
        user = None
        if username and password:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                raise ValueError(f"Username '{username}' already exists")

            user = User.objects.create_user(
                username=username,
                password=password,
                email=input.get('email', '')
            )

        # Create Employee with User link
        input['user'] = user
        employee = Employee.objects.create(**input)
        return employee

    @transaction.atomic
    def update(self, pk, input: dict):
        # Extract username and password from input if provided
        username = input.pop('username', None)
        password = input.pop('password', None)

        employee = Employee.objects.get(pk=pk)

        # Update User account if username and password provided
        if username and password:
            if employee.user:
                # Update existing user
                employee.user.username = username
                employee.user.set_password(password)
                employee.user.save()
            else:
                # Create new user for employee
                if User.objects.filter(username=username).exists():
                    raise ValueError(f"Username '{username}' already exists")

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=input.get('email', '')
                )
                employee.user = user

        # Update other fields
        for key, value in input.items():
            if hasattr(employee, key) and value is not None:
                setattr(employee, key, value)

        employee.save()
        return employee

    @transaction.atomic
    def delete(self, pk):
        employee = Employee.objects.get(pk=pk)
        # Also delete associated user account
        if employee.user:
            user = employee.user
            employee.user = None
            employee.save()
            user.delete()
        employee.delete()
