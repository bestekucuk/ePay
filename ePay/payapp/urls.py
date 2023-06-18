from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet
from .views import TransactionViewSet

app_name = 'payapp'

urlpatterns = [
    path('transactions/make_payment/', TransactionViewSet.as_view({'post': 'make_payment'}), name='make_payment'),
    path('transactions/list_transactions/', TransactionViewSet.as_view({'get': 'list_transactions'}), name='list_transactions'),
    path('transactions/account_summary/', TransactionViewSet.as_view({'get': 'account_summary'}), name='account_summary'),
]
