from django.urls import path
from . import views

urlpatterns = [
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction_add'),
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer_add'),
]
