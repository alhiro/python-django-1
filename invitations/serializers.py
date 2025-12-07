from rest_framework import serializers
from .models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id','email','role','token','created_at','expires_at','used','sender']
        read_only_fields = ['token','created_at','expires_at','used','sender']
