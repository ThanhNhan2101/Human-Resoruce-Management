from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from core.leaves.models import Leave, LeaveType
from core.employees.models import Employee
from django.forms import ModelForm, DateInput
from django import forms


class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }


class LeaveListView(LoginRequiredMixin, ListView):
    model = Leave
    template_name = 'leaves/leave_list.html'
    context_object_name = 'leaves'
    paginate_by = 10
    login_url = 'login'

    def get_queryset(self):
        queryset = Leave.objects.select_related(
            'employee', 'leave_type', 'approved_by')

        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search)
            )

        # Filter by status
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by leave type
        leave_type = self.request.GET.get('leave_type', '')
        if leave_type:
            queryset = queryset.filter(leave_type_id=leave_type)

        return queryset.order_by('-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leave_types'] = LeaveType.objects.all()
        context['statuses'] = Leave._meta.get_field('status').choices
        context['search'] = self.request.GET.get('search', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_leave_type'] = self.request.GET.get('leave_type', '')
        return context


class LeaveDetailView(LoginRequiredMixin, DetailView):
    model = Leave
    template_name = 'leaves/leave_detail.html'
    context_object_name = 'leave'
    login_url = 'login'


class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leaves/leave_form.html'
    success_url = reverse_lazy('leave_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Đăng ký nghỉ phép'
        context['button_text'] = 'Đăng ký'
        return context


class LeaveUpdateView(LoginRequiredMixin, UpdateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leaves/leave_form.html'
    success_url = reverse_lazy('leave_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cập nhật đơn nghỉ phép'
        context['button_text'] = 'Cập nhật'
        return context


class LeaveDeleteView(LoginRequiredMixin, DeleteView):
    model = Leave
    template_name = 'leaves/leave_confirm_delete.html'
    success_url = reverse_lazy('leave_list')
    login_url = 'login'


class LeaveApprovalView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, pk):
        leave = get_object_or_404(Leave, pk=pk)
        action = request.POST.get('action')

        if action == 'approve':
            leave.status = 'APPROVED'
            # Thay bằng request.user.employee profile
            leave.approved_by = Employee.objects.first()
        elif action == 'reject':
            leave.status = 'REJECTED'
            leave.remarks = request.POST.get('remarks', '')

        leave.save()
        return redirect('leave_detail', pk=pk)
