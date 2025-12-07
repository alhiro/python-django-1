from rest_framework import serializers
from .models import User
from invitations.models import Invitation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','role']

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    invitation_token = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        # If invitation token provided, verify it
        token = data.get('invitation_token')
        if token:
            try:
                inv = Invitation.objects.get(token=token, used=False)
            except Invitation.DoesNotExist:
                raise serializers.ValidationError('Invalid or used invitation token')
            if inv.is_expired():
                raise serializers.ValidationError('Invitation token expired')
            data['invitation_obj'] = inv
        return data

    def create(self, validated_data):
        inv = validated_data.pop('invitation_obj', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name',''),
        )

        if inv:
            user.role = inv.role
            user.save()
            inv.used = True
            inv.save()
        return user
