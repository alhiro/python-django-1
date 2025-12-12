from rest_framework import serializers
from .models import Invitation
from django.utils import timezone
from uuid import uuid4
from django.conf import settings

class InvitationSerializer(serializers.ModelSerializer):
    accept_url_demo = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = ['id', 'email', 'role', 'token', 'created_at', 'expires_at', 'used', 'sender', 'accept_url_demo']
        read_only_fields = ['token','created_at','expires_at','used','sender', 'accept_url_demo']
    
    def get_accept_url_demo(self, obj):
        frontend_url = settings.FRONTEND_URL
        return f"{frontend_url}/invite/{obj.token}"

    def create(self, validated_data):
        user = self.context['request'].user
        inv = Invitation.objects.create(
            sender=user,
            token=str(uuid4()),
            expires_at=timezone.now() + timezone.timedelta(hours=72),
            **validated_data
        )
        return inv
