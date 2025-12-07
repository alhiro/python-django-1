from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Create demo users: admin, manager, staff (password: pass1234)'

    def handle(self, *args, **options):
        demo = [
            ('admin','admin@example.com','admin'),
            ('manager','manager@example.com','manager'),
            ('staff','staff@example.com','staff'),
        ]
        for username,email,role in demo:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username,email=email,password='pass1234')
                user.role = role
                if role == 'admin':
                    user.is_superuser = True
                    user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created {username}'))
            else:
                self.stdout.write(f'{username} exists')
