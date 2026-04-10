from django.contrib import admin
from core.leaves.models import Leave


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date',
                    'duration_days', 'status')
    search_fields = ('employee__first_name', 'employee__last_name')
    list_filter = ('status', 'start_date')
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee',)
        }),
        ('Leave Period', {
            'fields': ('start_date', 'end_date', 'reason')
        }),
        ('Approval', {
            'fields': ('status', 'approved_by', 'remarks')
        }),
    )
