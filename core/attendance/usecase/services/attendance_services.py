from core.attendance.models import Attendance
from django.db import transaction
from dataclasses import dataclass


@dataclass
class AttendanceService:
    @transaction.atomic
    def create(self, input: dict):
        attendance = Attendance.objects.create(**input)
        return attendance

    @transaction.atomic
    def update(self, pk, input: dict):
        attendance = Attendance.objects.get(pk=pk)
        for key, value in input.items():
            if hasattr(attendance, key) and value is not None:
                setattr(attendance, key, value)
        attendance.save()
        return attendance

    @transaction.atomic
    def bulk_update_or_create(self, date, records: list):
        for record in records:
            Attendance.objects.update_or_create(
                employee=record['employee'],
                date=date,
                defaults={
                    'status': record.get('status', 'ABSENT'),
                    'check_in_time': record.get('check_in_time') or None,
                    'check_out_time': record.get('check_out_time') or None,
                    'notes': record.get('notes', ''),
                }
            )
