# Simple Admin Portal Backend (Django)

This is a minimal Django backend for the "Simple Admin Portal with RBAC & User Invitation".

## Features
- Custom User model with `role` (Admin / Manager / Staff)
- JWT authentication (djangorestframework-simplejwt)
- Models: User, Product, Order, Invitation
- Invitation flow: create token, send email (console backend), accept via registration endpoint
- Role-based permissions for APIs (Admin, Manager, Staff)
- Demo management command to create demo users (admin/manager/staff)

## Quick start (development)
1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Apply migrations and create demo data:
   ```bash
   export DJANGO_SECRET_KEY='dev-secret-key'
   python manage.py migrate
   python manage.py createsuperuser --username admin --email admin@example.com
   python manage.py create_demo_users
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

4. API endpoints (examples):
   - `POST /api/token/` — obtain JWT
   - `POST /api/token/refresh/` — refresh JWT
   - `POST /api/register/` — register (optionally with invitation token)
   - `GET /api/products/` — list products (RBAC enforced)
   - `POST /api/invitations/` — create invitation (Admin/Manager)
   - `POST /api/invitations/{id}/resend/` — resend invitation (Admin/Manager)
   - `POST /api/invitations/{id}/revoke/` — revoke (Admin/Manager)

## Invitation flow
- Invitation contains token, role, email, expiry (72 hours), and used flag.
- Emails are printed to console (Django's console email backend). To use SMTP, configure `EMAIL_BACKEND` in `settings.py`.
