from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.shop_reports, name='shop'),
]
