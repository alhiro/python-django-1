from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','product','quantity','created_by','created_at']
        read_only_fields = ['created_by','created_at']
