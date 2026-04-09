from django.urls import path
from core.employees.views.employee_views import (
    EmployeeListView,
    EmployeeDetailView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    DepartmentListView,
    DashboardView,
)

app_name = 'employees'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/<int:pk>/edit/',
         EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/delete/',
         EmployeeDeleteView.as_view(), name='employee_delete'),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
]
