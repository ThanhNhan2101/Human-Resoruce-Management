from django.contrib import admin
from core.attendance.models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in_time',
                    'check_out_time', 'status', 'working_hours')
    search_fields = ('employee__first_name', 'employee__last_name')
    list_filter = ('status', 'date')
    date_hierarchy = 'date'
