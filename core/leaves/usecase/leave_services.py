from core.leaves.models import Leave, LeaveType


def create_leave(employee, leave_type, start_date, end_date, reason):
    """Create a new leave request"""
    leave = Leave.objects.create(
        employee=employee,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        status='PENDING'
    )
    return leave


def approve_leave(leave_id, approved_by):
    """Approve a leave request"""
    leave = Leave.objects.get(id=leave_id)
    leave.status = 'APPROVED'
    leave.approved_by = approved_by
    leave.save()
    return leave


def reject_leave(leave_id, remarks):
    """Reject a leave request"""
    leave = Leave.objects.get(id=leave_id)
    leave.status = 'REJECTED'
    leave.remarks = remarks
    leave.save()
    return leave


def cancel_leave(leave_id):
    """Cancel a leave request"""
    leave = Leave.objects.get(id=leave_id)
    leave.status = 'CANCELLED'
    leave.save()
    return leave
