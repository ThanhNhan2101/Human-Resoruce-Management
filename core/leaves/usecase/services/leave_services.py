from core.leaves.models import Leave
from django.db import transaction
from django.core.exceptions import PermissionDenied
from dataclasses import dataclass


@dataclass
class LeaveService:
    @staticmethod
    def _is_admin(user):
        """Check if user is admin (is_staff or is_superuser)"""
        return user.is_staff or user.is_superuser

    @staticmethod
    def _check_leave_permission(leave, user, action='view'):
        """Check if user has permission to perform action on this leave"""
        is_admin = LeaveService._is_admin(user)
        is_owner = hasattr(
            user, 'employee') and leave.employee == user.employee

        if not is_admin and not is_owner:
            raise PermissionDenied(
                f"You don't have permission to {action} this leave request.")

    @transaction.atomic
    def create(self, input: dict, user=None):
        # If user is not admin, they can only create for themselves
        if user and not self._is_admin(user):
            if hasattr(user, 'employee') and user.employee:
                input['employee'] = user.employee
            else:
                raise PermissionDenied(
                    "Your user account is not linked to an employee record.")

        # Validate that employee is provided
        if 'employee' not in input or input['employee'] is None:
            raise ValueError("Employee is required to create a leave request.")

        leave = Leave.objects.create(**input)
        return leave

    @transaction.atomic
    def update(self, pk, input: dict, user=None):
        leave = Leave.objects.get(pk=pk)

        # Check permission
        if user:
            self._check_leave_permission(leave, user, 'update')

        # Don't allow non-admin to update status or approved_by
        if user and not self._is_admin(user):
            # Remove status-related fields from input
            input.pop('status', None)
            input.pop('approved_by', None)
            input.pop('remarks', None)
            input.pop('employee', None)  # Non-admin cannot change employee

        for key, value in input.items():
            if hasattr(leave, key) and value is not None:
                setattr(leave, key, value)
        leave.save()
        return leave

    @transaction.atomic
    def delete(self, pk, user=None):
        leave = Leave.objects.get(pk=pk)

        # Check permission
        if user:
            self._check_leave_permission(leave, user, 'delete')

        leave.delete()

    @transaction.atomic
    def approve(self, pk, approved_by, user=None):
        # Only admin can approve
        if user and not self._is_admin(user):
            raise PermissionDenied("Only admin can approve leave requests.")

        leave = Leave.objects.get(pk=pk)
        leave.status = 'APPROVED'
        leave.approved_by = approved_by
        leave.save()
        return leave

    @transaction.atomic
    def reject(self, pk, remarks='', user=None):
        # Only admin can reject
        if user and not self._is_admin(user):
            raise PermissionDenied("Only admin can reject leave requests.")

        leave = Leave.objects.get(pk=pk)
        leave.status = 'REJECTED'
        leave.remarks = remarks
        leave.save()
        return leave
