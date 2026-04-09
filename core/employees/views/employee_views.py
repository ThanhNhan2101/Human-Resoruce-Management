from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from core.employees.models import Employee, Department, Position
from django.forms import ModelForm, DateInput


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'gender', 'address', 'employee_id', 'department', 'position',
            'hire_date', 'status', 'base_salary', 'allowance', 'avatar'
        ]
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'hire_date': DateInput(attrs={'type': 'date'}),
        }


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10
    login_url = 'login'

    def get_queryset(self):
        queryset = Employee.objects.select_related('department', 'position')

        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(employee_id__icontains=search) |
                Q(email__icontains=search)
            )

        # Filter by department
        department = self.request.GET.get('department', '')
        if department:
            queryset = queryset.filter(department_id=department)

        # Filter by status
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['statuses'] = Employee.EMPLOYMENT_STATUS
        context['search'] = self.request.GET.get('search', '')
        context['selected_department'] = self.request.GET.get('department', '')
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attendances'] = self.object.attendances.all()[:10]
        context['leaves'] = self.object.leaves.all()[:5]
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Thêm nhân viên mới'
        context['button_text'] = 'Thêm'
        return context


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cập nhật thông tin nhân viên'
        context['button_text'] = 'Cập nhật'
        return context


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')
    login_url = 'login'


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'employees/department_list.html'
    context_object_name = 'departments'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for dept in context['departments']:
            dept.employee_count = dept.employees.count()
        return context


class DashboardView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        context = {
            'total_employees': Employee.objects.count(),
            'active_employees': Employee.objects.filter(status='ACTIVE').count(),
            'total_departments': Department.objects.count(),
            'total_positions': Position.objects.count(),
            'recent_employees': Employee.objects.all().order_by('-created_at')[:5],
        }
        return render(request, 'dashboard.html', context)
