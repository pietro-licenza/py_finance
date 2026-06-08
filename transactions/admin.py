"""Django Admin registration for the Transaction model."""

from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for the per-user financial transactions."""

    list_display = (
        'transaction_date',
        'description',
        'account',
        'category',
        'transaction_type',
        'amount',
    )
    list_filter = ('transaction_type', 'transaction_date', 'category')
    search_fields = ('description', 'account__name')
    date_hierarchy = 'transaction_date'
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-transaction_date',)

    fieldsets = (
        (None, {
            'fields': ('account', 'category', 'transaction_type'),
        }),
        ('Detalhes da transação', {
            'fields': ('amount', 'transaction_date', 'description'),
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
        }),
    )