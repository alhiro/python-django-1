from django.db import models
from django.utils import timezone
import uuid
from datetime import timedelta

class Invitation(models.Model):
    ROLE_CHOICES = [
        ('admin','Admin'),
        ('manager','Manager'),
        ('staff','Staff'),
    ]
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    sender = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self,*args,**kwargs):
        if not self.expires_at:
            self.expires_at = self.created_at + timedelta(hours=72)
        super().save(*args,**kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at
