from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.serializers import MyTokenObtainPairView

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('invitations.urls')),
    path('api/', include('users.urls')),
]
