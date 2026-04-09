from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from core.attendance.models import Attendance
from core.employees.models import Employee
from django.forms import ModelForm, DateInput, TimeInput
from django import forms
from django.utils import timezone
from datetime import datetime, timedelta


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


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendances'
    paginate_by = 15
    login_url = 'login'

    def get_queryset(self):
        queryset = Attendance.objects.select_related(
            'employee').order_by('-date')

        # Filter by employee
        employee = self.request.GET.get('employee', '')
        if employee:
            queryset = queryset.filter(employee_id=employee)

        # Filter by status
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by date range
        from_date = self.request.GET.get('from_date', '')
        to_date = self.request.GET.get('to_date', '')

        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Employee.objects.all()
        context['statuses'] = Attendance.STATUS_CHOICES
        context['from_date'] = self.request.GET.get('from_date', '')
        context['to_date'] = self.request.GET.get('to_date', '')
        context['selected_employee'] = self.request.GET.get('employee', '')
        context['selected_status'] = self.request.GET.get('status', '')

        # Calculate statistics
        context['today_present'] = Attendance.objects.filter(
            date=timezone.now().date(),
            status='PRESENT'
        ).count()
        context['today_absent'] = Attendance.objects.filter(
            date=timezone.now().date(),
            status='ABSENT'
        ).count()

        return context


class AttendanceDetailView(LoginRequiredMixin, DetailView):
    model = Attendance
    template_name = 'attendance/attendance_detail.html'
    context_object_name = 'attendance'
    login_url = 'login'


class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance/attendance_form.html'
    success_url = reverse_lazy('attendance_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Thêm chấm công'
        context['button_text'] = 'Thêm'
        return context


class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance/attendance_form.html'
    success_url = reverse_lazy('attendance_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cập nhật chấm công'
        context['button_text'] = 'Cập nhật'
        return context


class DailyAttendanceView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        today = timezone.now().date()
        attendances = Attendance.objects.filter(
            date=today).select_related('employee')

        from_date = request.GET.get('date', today.isoformat())
        return render(request, 'attendance/daily_attendance.html', {
            'attendances': attendances,
            'date': from_date,
            'statuses': Attendance.STATUS_CHOICES,
        })

    def post(self, request):
        date = request.POST.get('date', timezone.now().date())
        employees = Employee.objects.filter(status='ACTIVE')

        for employee in employees:
            status = request.POST.get(f'status_{employee.id}', 'ABSENT')
            check_in = request.POST.get(f'check_in_{employee.id}', '')
            check_out = request.POST.get(f'check_out_{employee.id}', '')
            notes = request.POST.get(f'notes_{employee.id}', '')

            Attendance.objects.update_or_create(
                employee=employee,
                date=date,
                defaults={
                    'status': status,
                    'check_in_time': check_in or None,
                    'check_out_time': check_out or None,
                    'notes': notes,
                }
            )

        return redirect('attendance:attendance_list')
