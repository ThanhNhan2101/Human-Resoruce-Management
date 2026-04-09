from django.urls import path
from core.attendance.views.attendance_views import (
    AttendanceListView,
    AttendanceDetailView,
    AttendanceCreateView,
    AttendanceUpdateView,
    DailyAttendanceView,
)

app_name = 'attendance'

urlpatterns = [
    path('', AttendanceListView.as_view(), name='attendance_list'),
    path('daily/', DailyAttendanceView.as_view(), name='daily_attendance'),
    path('create/', AttendanceCreateView.as_view(), name='attendance_create'),
    path('<int:pk>/', AttendanceDetailView.as_view(), name='attendance_detail'),
    path('<int:pk>/edit/', AttendanceUpdateView.as_view(), name='attendance_edit'),
]
