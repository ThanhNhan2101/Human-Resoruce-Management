from core.employees.models import Employee, Department, Position


def create_employee(first_name, last_name, email, phone, date_of_birth, gender,
                    address, employee_id, department, position, hire_date,
                    base_salary, allowance, **kwargs):
    """Create a new employee"""
    employee = Employee.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        date_of_birth=date_of_birth,
        gender=gender,
        address=address,
        employee_id=employee_id,
        department=department,
        position=position,
        hire_date=hire_date,
        base_salary=base_salary,
        allowance=allowance,
    )
    return employee


def update_employee(employee_id, **kwargs):
    """Update employee information"""
    employee = Employee.objects.get(id=employee_id)
    for key, value in kwargs.items():
        if hasattr(employee, key) and value is not None:
            setattr(employee, key, value)
    employee.save()
    return employee


def delete_employee(employee_id):
    """Delete an employee"""
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return True
