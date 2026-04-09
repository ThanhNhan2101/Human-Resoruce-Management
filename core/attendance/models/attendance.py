from django.db import models
from core.employees.models import Employee
from django.utils import timezone


class Attendance(models.Model):
    """Attendance model"""

    STATUS_CHOICES = [
        ('PRESENT', 'Có mặt'),
        ('ABSENT', 'Vắng mặt'),
        ('LATE', 'Đi muộn'),
        ('EARLY_LEAVE', 'Về sớm'),
        ('HALF_DAY', 'Nửa ngày'),
        ('ON_LEAVE', 'Đang nghỉ phép'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    date = models.DateField(db_index=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ABSENT'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.status})"

    @property
    def working_hours(self):
        if self.check_in_time and self.check_out_time:
            from datetime import datetime, timedelta
            check_in = datetime.combine(
                timezone.now().date(), self.check_in_time)
            check_out = datetime.combine(
                timezone.now().date(), self.check_out_time)
            duration = check_out - check_in
            hours = duration.total_seconds() / 3600
            return round(hours, 2)
        return None
