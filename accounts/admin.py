"""Django Admin registration for the Account model."""

from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Admin interface for the per-user bank accounts."""

    list_display = (
        'user',
        'name',
        'bank_name',
        'account_type',
        'balance',
        'is_active',
    )
    list_filter = ('account_type', 'is_active')
    search_fields = ('name', 'bank_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'bank_name', 'account_type'),
        }),
        ('Detalhes financeiros', {
            'fields': ('balance', 'is_active'),
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
