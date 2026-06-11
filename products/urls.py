from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('catalog/', views.catalog, name='catalog'),
    path('new/', views.product_create, name='create'),
    path('<int:pk>/edit/', views.product_update, name='update'),
]
