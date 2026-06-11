from django.urls import path

from . import views

app_name = 'credits'

urlpatterns = [
    path('', views.credit_list, name='list'),
    path('<int:pk>/extension/', views.request_extension, name='extension'),
]
