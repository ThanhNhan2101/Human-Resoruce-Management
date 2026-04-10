from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from core.attendance.models import Attendance
from core.employees.models import Employee
from django.forms import ModelForm, DateInput, TimeInput
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator

from core.attendance.usecase.selectors.attendance_selectors import AttendanceSelector
from core.attendance.usecase.services.attendance_services import AttendanceService
from core.employees.usecase.selectors.employee_selectors import EmployeeSelector


class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'check_in_time',
                  'check_out_time', 'status', 'notes']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'check_in_time': TimeInput(attrs={'type': 'time'}),
            'check_out_time': TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class AttendanceListView(LoginRequiredMixin, View):
    template_name = 'attendance/attendance_list.html'
    login_url = 'login'

    def get(self, request):
        selector = AttendanceSelector()
        filters = {
            'employee': request.GET.get('employee', ''),
            'status': request.GET.get('status', ''),
            'from_date': request.GET.get('from_date', ''),
            'to_date': request.GET.get('to_date', ''),
        }
        attendances = selector.list(filters=filters)

        paginator = Paginator(attendances, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        emp_selector = EmployeeSelector()
        context = {
            'attendances': page_obj,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'employees': emp_selector.list(),
            'statuses': Attendance.STATUS_CHOICES,
            'from_date': filters['from_date'],
            'to_date': filters['to_date'],
            'selected_employee': filters['employee'],
            'selected_status': filters['status'],
            'today_present': selector.get_today_by_status('PRESENT'),
            'today_absent': selector.get_today_by_status('ABSENT'),
        }
        return render(request, self.template_name, context)


class AttendanceDetailView(LoginRequiredMixin, View):
    template_name = 'attendance/attendance_detail.html'
    login_url = 'login'

    def get(self, request, pk):
        selector = AttendanceSelector()
        attendance = selector.get_by_id(pk)
        return render(request, self.template_name, {'attendance': attendance})


class AttendanceCreateView(LoginRequiredMixin, FormView):
    template_name = 'attendance/attendance_form.html'
    form_class = AttendanceForm
    success_url = reverse_lazy('attendance:attendance_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Thêm chấm công'
        context['button_text'] = 'Thêm'
        return context

    def form_valid(self, form):
        service = AttendanceService()
        service.create(input=form.cleaned_data)
        return redirect(self.success_url)


class AttendanceUpdateView(LoginRequiredMixin, FormView):
    template_name = 'attendance/attendance_form.html'
    form_class = AttendanceForm
    success_url = reverse_lazy('attendance:attendance_list')
    login_url = 'login'

    def get_form(self, form_class=None):
        selector = AttendanceSelector()
        self.attendance = selector.get_by_id(self.kwargs['pk'])
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.attendance, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cập nhật chấm công'
        context['button_text'] = 'Cập nhật'
        return context

    def form_valid(self, form):
        service = AttendanceService()
        service.update(pk=self.kwargs['pk'], input=form.cleaned_data)
        return redirect(self.success_url)


class DailyAttendanceView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        today = timezone.now().date()
        selector = AttendanceSelector()
        attendances = selector.get_by_date(today)

        from_date = request.GET.get('date', today.isoformat())
        return render(request, 'attendance/daily_attendance.html', {
            'attendances': attendances,
            'date': from_date,
            'statuses': Attendance.STATUS_CHOICES,
        })

    def post(self, request):
        date = request.POST.get('date', timezone.now().date())
        emp_selector = EmployeeSelector()
        employees = emp_selector.get_active()

        records = []
        for employee in employees:
            records.append({
                'employee': employee,
                'status': request.POST.get(f'status_{employee.id}', 'ABSENT'),
                'check_in_time': request.POST.get(f'check_in_{employee.id}', ''),
                'check_out_time': request.POST.get(f'check_out_{employee.id}', ''),
                'notes': request.POST.get(f'notes_{employee.id}', ''),
            })

        service = AttendanceService()
        service.bulk_update_or_create(date=date, records=records)
        return redirect('attendance:attendance_list')
