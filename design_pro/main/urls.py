from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_request/', views.create_request, name='create_request'),
    path('my_requests/', views.my_requests, name='my_requests'),
    path('profile/', views.profile, name='profile'),
]