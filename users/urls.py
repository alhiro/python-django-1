from django.urls import path
from .views import (
    UserListCreateView,
    UserDetailView,
    ProfileView,
    RegisterView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('users/', UserListCreateView.as_view(), name='user_list_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/', ProfileView.as_view(), name='user_profile'),
]
