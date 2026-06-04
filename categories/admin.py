"""Django Admin registration for the Category model."""

from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for the per-user transaction categories."""

    list_display = (
        'user',
        'name',
        'category_type',
        'color',
        'created_at',
        'updated_at',
    )
    list_filter = ('category_type',)
    search_fields = ('name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('category_type', 'name')

    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'category_type', 'color'),
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
