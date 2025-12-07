from django.contrib import admin
from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email','role','token','created_at','expires_at','used')
    readonly_fields = ('token','created_at')
