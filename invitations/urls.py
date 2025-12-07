from django.urls import path, include
from rest_framework import routers
from .views import InvitationViewSet

router = routers.DefaultRouter()
router.register(r'invitations', InvitationViewSet, basename='invitations')

urlpatterns = [
    path('', include(router.urls)),
]
