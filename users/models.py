from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_STAFF = 'staff'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_STAFF, 'Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STAFF)

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_manager(self):
        return self.role == self.ROLE_MANAGER

    def is_staff_role(self):
        return self.role == self.ROLE_STAFF
