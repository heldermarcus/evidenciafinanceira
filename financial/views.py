from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .models import Transaction, Category, Customer

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'financial/transaction_form.html'
    fields = ['type', 'account', 'category', 'amount', 'date', 'payment_method', 'description']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # When a transaction is created, change the balance of the account
        response = super().form_valid(form)
        
        account = self.object.account
        if self.object.type == 'income':
            account.balance += self.object.amount
        elif self.object.type == 'expense':
            account.balance -= self.object.amount
        # Transfer type logic will be handled later
        account.save()
        
        return response

    def get_initial(self):
        initial = super().get_initial()
        # default to today
        from django.utils import timezone
        initial['date'] = timezone.now().date()
        return initial

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'financial/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        # Customers for the user's active store
        store = self.request.user.stores.first()
        if store:
            return Customer.objects.filter(store=store)
        return Customer.objects.none()

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'financial/customer_form.html'
    fields = ['name', 'cpf', 'phone', 'address', 'notes']
    success_url = reverse_lazy('customer_list')

    def form_valid(self, form):
        store = self.request.user.stores.first()
        form.instance.store = store
        return super().form_valid(form)
