from core.leaves.models import Leave
from django.db.models import Q
from django.shortcuts import get_object_or_404


class LeaveSelector:
    def list(self, filters=None):
        filters = filters or {}
        queryset = Leave.objects.select_related('employee', 'approved_by')

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

    def get_by_id(self, pk):
        return get_object_or_404(
            Leave.objects.select_related('employee', 'approved_by'),
            pk=pk
        )
