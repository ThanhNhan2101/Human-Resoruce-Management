from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from core.leaves.models import Leave
from core.employees.models import Employee
from django.forms import ModelForm, DateInput
from django import forms
from django.core.paginator import Paginator

from core.leaves.usecase.selectors.leave_selectors import LeaveSelector
from core.leaves.usecase.services.leave_services import LeaveService


class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }


class LeaveListView(LoginRequiredMixin, View):
    template_name = 'leaves/leave_list.html'
    login_url = 'login'

    def get(self, request):
        selector = LeaveSelector()
        filters = {
            'search': request.GET.get('search', ''),
            'status': request.GET.get('status', ''),
        }
        leaves = selector.list(filters=filters, user=request.user)

        paginator = Paginator(leaves, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Check if user is admin
        is_admin = request.user.is_staff or request.user.is_superuser

        context = {
            'leaves': page_obj,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'statuses': Leave.STATUS_CHOICES,
            'search': filters['search'],
            'selected_status': filters['status'],
            'is_admin': is_admin,
        }
        return render(request, self.template_name, context)


class LeaveDetailView(LoginRequiredMixin, View):
    template_name = 'leaves/leave_detail.html'
    login_url = 'login'

    def get(self, request, pk):
        selector = LeaveSelector()
        try:
            leave = selector.get_by_id(pk, user=request.user)
        except PermissionDenied:
            raise PermissionDenied(
                "You don't have permission to view this leave request.")

        is_admin = request.user.is_staff or request.user.is_superuser

        context = {
            'leave': leave,
            'is_admin': is_admin,
        }
        return render(request, self.template_name, context)


class LeaveCreateView(LoginRequiredMixin, FormView):
    template_name = 'leaves/leave_form.html'
    form_class = LeaveForm
    success_url = reverse_lazy('leaves:leave_list')
    login_url = 'login'

    def get_form(self, form_class=None):
        """Customize form for non-admin users"""
        form = super().get_form(form_class)
        is_admin = self.request.user.is_staff or self.request.user.is_superuser

        # Non-admin users can only create for themselves
        if not is_admin:
            if not (hasattr(self.request.user, 'employee') and self.request.user.employee):
                raise PermissionDenied(
                    "Your user account is not linked to an employee record.")
            # Remove employee field for non-admin users
            del form.fields['employee']

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Request Leave'
        context['button_text'] = 'Đăng ký'
        return context

    def form_valid(self, form):
        service = LeaveService()
        service.create(input=form.cleaned_data, user=self.request.user)
        return redirect(self.success_url)


class LeaveUpdateView(LoginRequiredMixin, FormView):
    template_name = 'leaves/leave_form.html'
    form_class = LeaveForm
    success_url = reverse_lazy('leaves:leave_list')
    login_url = 'login'

    def get_form(self, form_class=None):
        selector = LeaveSelector()
        try:
            self.leave = selector.get_by_id(
                self.kwargs['pk'], user=self.request.user)
        except PermissionDenied:
            raise PermissionDenied(
                "You don't have permission to edit this leave request.")

        is_admin = self.request.user.is_staff or self.request.user.is_superuser

        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(instance=self.leave, **self.get_form_kwargs())

        # Non-admin users can only edit certain fields
        if not is_admin:
            # Remove employee field for non-admin users
            del form.fields['employee']

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Updated đơn nghỉ phép'
        context['button_text'] = 'Updated'
        return context

    def form_valid(self, form):
        service = LeaveService()
        service.update(
            pk=self.kwargs['pk'], input=form.cleaned_data, user=self.request.user)
        return redirect(self.success_url)


class LeaveDeleteView(LoginRequiredMixin, View):
    template_name = 'leaves/leave_confirm_delete.html'
    login_url = 'login'

    def get(self, request, pk):
        selector = LeaveSelector()
        try:
            leave = selector.get_by_id(pk, user=request.user)
        except PermissionDenied:
            raise PermissionDenied(
                "You don't have permission to delete this leave request.")

        return render(request, self.template_name, {'leave': leave})

    def post(self, request, pk):
        service = LeaveService()
        try:
            service.delete(pk=pk, user=request.user)
        except PermissionDenied:
            raise PermissionDenied(
                "You don't have permission to delete this leave request.")

        return redirect('leaves:leave_list')


class LeaveApprovalView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, pk):
        # Only admin can approve/reject
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied(
                "Only admin can approve/reject leave requests.")

        service = LeaveService()
        action = request.POST.get('action')

        if action == 'approve':
            approved_by = request.user.employee if hasattr(
                request.user, 'employee') else Employee.objects.first()
            service.approve(pk=pk, approved_by=approved_by, user=request.user)
        elif action == 'reject':
            remarks = request.POST.get('remarks', '')
            service.reject(pk=pk, remarks=remarks, user=request.user)

        return redirect('leaves:leave_detail', pk=pk)
