from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from core.employees.models import Employee, Department, Position
from django.forms import ModelForm, DateInput
from django.core.paginator import Paginator

from core.employees.usecase.selectors.employee_selectors import EmployeeSelector, DepartmentSelector
from core.employees.usecase.services.employee_services import EmployeeService


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


class EmployeeListView(LoginRequiredMixin, View):
    template_name = 'employees/employee_list.html'
    login_url = 'login'

    def get(self, request):
        selector = EmployeeSelector()
        filters = {
            'search': request.GET.get('search', ''),
            'department': request.GET.get('department', ''),
            'status': request.GET.get('status', ''),
        }
        employees = selector.list(filters=filters)

        paginator = Paginator(employees, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        dept_selector = DepartmentSelector()
        context = {
            'employees': page_obj,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'departments': dept_selector.list(),
            'statuses': Employee.EMPLOYMENT_STATUS,
            'search': filters['search'],
            'selected_department': filters['department'],
            'selected_status': filters['status'],
        }
        return render(request, self.template_name, context)


class EmployeeDetailView(LoginRequiredMixin, View):
    template_name = 'employees/employee_detail.html'
    login_url = 'login'

    def get(self, request, pk):
        selector = EmployeeSelector()
        employee = selector.get_by_id(pk)
        context = {
            'employee': employee,
            'attendances': employee.attendances.all()[:10],
            'leaves': employee.leaves.all()[:5],
        }
        return render(request, self.template_name, context)


class EmployeeCreateView(LoginRequiredMixin, FormView):
    template_name = 'employees/employee_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employees:employee_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Thêm nhân viên mới'
        context['button_text'] = 'Thêm'
        return context

    def form_valid(self, form):
        service = EmployeeService()
        service.create(input=form.cleaned_data)
        return redirect(self.success_url)


class EmployeeUpdateView(LoginRequiredMixin, FormView):
    template_name = 'employees/employee_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employees:employee_list')
    login_url = 'login'

    def get_form(self, form_class=None):
        selector = EmployeeSelector()
        self.employee = selector.get_by_id(self.kwargs['pk'])
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.employee, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cập nhật thông tin nhân viên'
        context['button_text'] = 'Cập nhật'
        return context

    def form_valid(self, form):
        service = EmployeeService()
        service.update(pk=self.kwargs['pk'], input=form.cleaned_data)
        return redirect(self.success_url)


class EmployeeDeleteView(LoginRequiredMixin, View):
    template_name = 'employees/employee_confirm_delete.html'
    login_url = 'login'

    def get(self, request, pk):
        selector = EmployeeSelector()
        employee = selector.get_by_id(pk)
        return render(request, self.template_name, {'employee': employee})

    def post(self, request, pk):
        service = EmployeeService()
        service.delete(pk=pk)
        return redirect('employees:employee_list')


class DepartmentListView(LoginRequiredMixin, View):
    template_name = 'employees/department_list.html'
    login_url = 'login'

    def get(self, request):
        selector = DepartmentSelector()
        departments = selector.list()
        for dept in departments:
            dept.employee_count = dept.employees.count()
        context = {'departments': departments}
        return render(request, self.template_name, context)


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
