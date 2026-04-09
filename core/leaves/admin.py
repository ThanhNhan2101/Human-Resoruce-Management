from django.contrib import admin
from core.leaves.models import Leave, LeaveType


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'days_per_year', 'is_paid')
    search_fields = ('name',)


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date',
                    'end_date', 'duration_days', 'status')
    search_fields = ('employee__first_name', 'employee__last_name')
    list_filter = ('status', 'leave_type', 'start_date')
    fieldsets = (
        ('Thông tin nhân viên', {
            'fields': ('employee', 'leave_type')
        }),
        ('Thời gian nghỉ', {
            'fields': ('start_date', 'end_date', 'reason')
        }),
        ('Duyệt phép', {
            'fields': ('status', 'approved_by', 'remarks')
        }),
    )
