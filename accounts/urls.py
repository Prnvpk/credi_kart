from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('shopkeepers/', views.shopkeeper_approvals, name='shopkeeper_approvals'),
    path('shopkeepers/<int:pk>/toggle/', views.toggle_shopkeeper, name='toggle_shopkeeper'),
]
