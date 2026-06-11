from django.urls import path

from . import views

app_name = 'chat_system'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
]
