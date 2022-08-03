from django.urls import path
from . import views

urlpatterns = [
    path('add-post', views.add_post, name='add_post'),
    path('update-post/<str:pk>/', views.update_post, name='update_post'),
    path('delete-post/<str:pk>/', views.delete_post, name='delete_post'),
    path('<str:pk>/', views.show_post, name='post')
]
