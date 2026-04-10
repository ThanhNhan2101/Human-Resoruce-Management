from core.leaves.models import Leave
from django.db import transaction
from dataclasses import dataclass


@dataclass
class LeaveService:
    @transaction.atomic
    def create(self, input: dict):
        leave = Leave.objects.create(**input)
        return leave

    @transaction.atomic
    def update(self, pk, input: dict):
        leave = Leave.objects.get(pk=pk)
        for key, value in input.items():
            if hasattr(leave, key) and value is not None:
                setattr(leave, key, value)
        leave.save()
        return leave

    @transaction.atomic
    def delete(self, pk):
        leave = Leave.objects.get(pk=pk)
        leave.delete()

    @transaction.atomic
    def approve(self, pk, approved_by):
        leave = Leave.objects.get(pk=pk)
        leave.status = 'APPROVED'
        leave.approved_by = approved_by
        leave.save()
        return leave

    @transaction.atomic
    def reject(self, pk, remarks=''):
        leave = Leave.objects.get(pk=pk)
        leave.status = 'REJECTED'
        leave.remarks = remarks
        leave.save()
        return leave
