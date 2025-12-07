from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Simple RBAC enforcement: Admin full, Manager can edit, Staff read-only

class IsReadOnlyForStaff:
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role == 'staff' and request.method not in ('GET','HEAD','OPTIONS'):
            return False
        return True

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        return [IsAuthenticated(), IsReadOnlyForStaff()]
