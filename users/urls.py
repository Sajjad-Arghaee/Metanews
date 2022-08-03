from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('accout/', views.account, name='account'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('send-message/<str:pk>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('read-message/<str:pk>/', views.read_message, name='read_message'),
    path('<str:pk>/', views.show_profile, name='profile'),
]
