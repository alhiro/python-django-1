from rest_framework import viewsets, status
from .models import Invitation
from .serializers import InvitationSerializer
from rest_framework.decorators import action
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
        # list and retrieve allowed for authenticated users; create/resend/revoke restricted
        if self.action in ['create','resend','revoke']:
            permission_classes = [IsAdminOrManager]
        else:
            permission_classes = [IsAdminOrManager]
        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        # create token and expiry
        token = str(uuid4())
        sender = self.request.user
        inv = serializer.save(token=token, sender=sender)
        # ensure expiry
        inv.expires_at = inv.created_at + timezone.timedelta(hours=72)
        inv.save()
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

    def _send_invite_email(self, inv):
        # For development we use console email backend.
        accept_url = f"http://localhost:3000/accept-invite?token={inv.token}"
        subject = 'You are invited'
        msg = f'You have been invited as {inv.role}. Click to accept: {accept_url}'
        send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, [inv.email])
