from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('record/<int:credit_id>/', views.record_payment, name='record'),
]
