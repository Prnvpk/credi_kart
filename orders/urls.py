from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('checkout/', views.checkout, name='checkout'),
    path('<int:pk>/receipt/', views.receipt, name='receipt'),
]
