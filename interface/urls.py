from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('topic/<str:pk>/', views.topic, name='topic'),
    path('post/', include('posts.urls')),
    path('users/', include('users.urls')),
]
