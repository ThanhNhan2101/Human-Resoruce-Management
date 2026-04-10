from django.contrib import admin
from core.employees.models import Employee, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'email',
                    'department', 'position', 'status', 'hire_date')
    search_fields = ('employee_id', 'first_name', 'last_name', 'email')
    list_filter = ('status', 'department', 'gender', 'hire_date')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender', 'address', 'avatar')
        }),
        ('Employment Information', {
            'fields': ('employee_id', 'department', 'position', 'hire_date', 'status')
        }),
        ('Salary Information', {
            'fields': ('base_salary', 'allowance')
        }),
    )
