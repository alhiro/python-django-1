from email.message import EmailMessage
from rest_framework import viewsets, status
from .models import Invitation
from .serializers import InvitationSerializer
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import IsAdminOrManager
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from uuid import uuid4

class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all().order_by('-created_at')
    serializer_class = InvitationSerializer

    def get_permissions(self):
        # list and retrieve allowed for authenticated users
        if self.action in ['create','resend','revoke']:
            permission_classes = [IsAdminOrManager]
        else:
            permission_classes = [IsAdminOrManager]
        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        inv = serializer.save() 
        self._send_invite_email(inv)

    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        inv = self.get_object()
        if inv.used:
            return Response({'detail':'Invitation already used'}, status=status.HTTP_400_BAD_REQUEST)
        if inv.is_expired():
            inv.token = str(uuid4())
            inv.created_at = timezone.now()
            inv.expires_at = inv.created_at + timezone.timedelta(hours=72)
            inv.save()
        self._send_invite_email(inv)
        return Response({'detail':'Resent'})

    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        inv = self.get_object()
        inv.used = True
        inv.save()
        return Response({'detail':'Revoked'})

    # def _send_invite_email(self, inv):
    #     accept_url = f"http://localhost:3000/invite?token={inv.token}"
    #     subject = 'You are invited'
    #     body = f'You have been invited as {inv.role}. Click to accept: {accept_url}'
        
    #     email = EmailMessage(
    #         subject=subject,
    #         body=body,
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         to=[inv.email],
    #     )
    #     email.send()

    def _send_invite_email(self, inv):
        accept_url = f"http://localhost:3000/invite/{inv.token}"
        message = f'You have been invited as {inv.role}. Click to accept: {accept_url}'
        # fallback to message. for demo only
        return message, accept_url

@api_view(['GET'])
def validate_invitation(request):
    token = request.query_params.get('token')
    if not token:
        return Response({'detail': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        inv = Invitation.objects.get(token=token)
        if inv.is_expired() or inv.used:
            return Response({'detail': 'Token invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'email': inv.email, 'role': inv.role, 'token': inv.token})
    except Invitation.DoesNotExist:
        return Response({'detail': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)