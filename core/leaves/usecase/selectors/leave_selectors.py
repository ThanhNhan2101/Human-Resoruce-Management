from core.leaves.models import Leave
from django.db.models import Q
from django.shortcuts import get_object_or_404


class LeaveSelector:
    def list(self, filters=None, user=None):
        filters = filters or {}
        queryset = Leave.objects.select_related('employee', 'approved_by')

        # Filter by user role: non-admin sees only their own leaves
        if user and not self._is_admin(user):
            if hasattr(user, 'employee'):
                queryset = queryset.filter(employee=user.employee)

        search = filters.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search)
            )

        status = filters.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-start_date')

    def get_by_id(self, pk, user=None):
        leave = get_object_or_404(
            Leave.objects.select_related('employee', 'approved_by'),
            pk=pk
        )

        # Check permission: non-admin can only see their own leaves
        if user and not self._is_admin(user):
            if hasattr(user, 'employee') and leave.employee != user.employee:
                raise get_object_or_404(Leave, pk=None)  # Returns 404

        return leave

    @staticmethod
    def _is_admin(user):
        """Check if user is admin (is_staff or is_superuser)"""
        return user.is_staff or user.is_superuser
