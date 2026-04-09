from django.urls import path
from core.leaves.views.leave_views import (
    LeaveListView,
    LeaveDetailView,
    LeaveCreateView,
    LeaveUpdateView,
    LeaveDeleteView,
    LeaveApprovalView,
)

app_name = 'leaves'

urlpatterns = [
    path('', LeaveListView.as_view(), name='leave_list'),
    path('create/', LeaveCreateView.as_view(), name='leave_create'),
    path('<int:pk>/', LeaveDetailView.as_view(), name='leave_detail'),
    path('<int:pk>/edit/', LeaveUpdateView.as_view(), name='leave_edit'),
    path('<int:pk>/delete/', LeaveDeleteView.as_view(), name='leave_delete'),
    path('<int:pk>/approve/', LeaveApprovalView.as_view(), name='leave_approve'),
]
