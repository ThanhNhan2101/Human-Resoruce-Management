from core.attendance.models import Attendance
from django.shortcuts import get_object_or_404
from django.utils import timezone


class AttendanceSelector:
    def list(self, filters=None):
        filters = filters or {}
        queryset = Attendance.objects.select_related(
            'employee').order_by('-date')

        employee = filters.get('employee', '')
        if employee:
            queryset = queryset.filter(employee_id=employee)

        status = filters.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        from_date = filters.get('from_date', '')
        if from_date:
            queryset = queryset.filter(date__gte=from_date)

        to_date = filters.get('to_date', '')
        if to_date:
            queryset = queryset.filter(date__lte=to_date)

        return queryset

    def get_by_id(self, pk):
        return get_object_or_404(
            Attendance.objects.select_related('employee'),
            pk=pk
        )

    def get_today_by_status(self, status):
        return Attendance.objects.filter(
            date=timezone.now().date(),
            status=status
        ).count()

    def get_by_date(self, date):
        return Attendance.objects.filter(date=date).select_related('employee')
