from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin for the per-user Profile model."""

    list_display = ('user', 'full_name', 'phone', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'full_name')
    ordering = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')
