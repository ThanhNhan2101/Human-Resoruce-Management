from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from core.leaves.models import Leave, LeaveType
from core.employees.models import Employee
from django.forms import ModelForm, DateInput
from django import forms
from django.core.paginator import Paginator

from core.leaves.usecase.selectors.leave_selectors import LeaveSelector, LeaveTypeSelector
from core.leaves.usecase.services.leave_services import LeaveService


class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
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
            'leave_type': request.GET.get('leave_type', ''),
        }
        leaves = selector.list(filters=filters)

        paginator = Paginator(leaves, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        type_selector = LeaveTypeSelector()
        context = {
            'leaves': page_obj,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'leave_types': type_selector.list(),
            'statuses': Leave.STATUS_CHOICES,
            'search': filters['search'],
            'selected_status': filters['status'],
            'selected_leave_type': filters['leave_type'],
        }
        return render(request, self.template_name, context)


class LeaveDetailView(LoginRequiredMixin, View):
    template_name = 'leaves/leave_detail.html'
    login_url = 'login'

    def get(self, request, pk):
        selector = LeaveSelector()
        leave = selector.get_by_id(pk)
        return render(request, self.template_name, {'leave': leave})


class LeaveCreateView(LoginRequiredMixin, FormView):
    template_name = 'leaves/leave_form.html'
    form_class = LeaveForm
    success_url = reverse_lazy('leaves:leave_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Đăng ký nghỉ phép'
        context['button_text'] = 'Đăng ký'
        return context

    def form_valid(self, form):
        service = LeaveService()
        service.create(input=form.cleaned_data)
        return redirect(self.success_url)


class LeaveUpdateView(LoginRequiredMixin, FormView):
    template_name = 'leaves/leave_form.html'
    form_class = LeaveForm
    success_url = reverse_lazy('leaves:leave_list')
    login_url = 'login'

    def get_form(self, form_class=None):
        selector = LeaveSelector()
        self.leave = selector.get_by_id(self.kwargs['pk'])
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.leave, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cập nhật đơn nghỉ phép'
        context['button_text'] = 'Cập nhật'
        return context

    def form_valid(self, form):
        service = LeaveService()
        service.update(pk=self.kwargs['pk'], input=form.cleaned_data)
        return redirect(self.success_url)


class LeaveDeleteView(LoginRequiredMixin, View):
    template_name = 'leaves/leave_confirm_delete.html'
    login_url = 'login'

    def get(self, request, pk):
        selector = LeaveSelector()
        leave = selector.get_by_id(pk)
        return render(request, self.template_name, {'leave': leave})

    def post(self, request, pk):
        service = LeaveService()
        service.delete(pk=pk)
        return redirect('leaves:leave_list')


class LeaveApprovalView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, pk):
        service = LeaveService()
        action = request.POST.get('action')

        if action == 'approve':
            approved_by = Employee.objects.first()
            service.approve(pk=pk, approved_by=approved_by)
        elif action == 'reject':
            remarks = request.POST.get('remarks', '')
            service.reject(pk=pk, remarks=remarks)

        return redirect('leaves:leave_detail', pk=pk)
