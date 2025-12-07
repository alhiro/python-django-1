from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

# Order RBAC: Admin and Manager can create/edit; Staff read-only
class OrderRolePermission:
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role == 'staff' and request.method not in ('GET','HEAD','OPTIONS'):
            return False
        return True

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def get_permissions(self):
        return [IsAuthenticated(), OrderRolePermission()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
