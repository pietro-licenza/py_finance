"""
Category model for the Finanpy project.

Represents a user-owned category used to classify transactions as
either income or expense. Categories are scoped per user so the same
name (e.g. "Alimentação") can be reused across different users.
"""

from django.conf import settings
from django.db import models


class Category(models.Model):
    """A user-defined classification for transactions."""

    class CategoryType(models.TextChoices):
        INCOME = 'INCOME', 'Receita'
        EXPENSE = 'EXPENSE', 'Despesa'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='usuário',
    )
    name = models.CharField(
        max_length=50,
        verbose_name='nome',
    )
    category_type = models.CharField(
        max_length=20,
        choices=CategoryType.choices,
        verbose_name='tipo',
    )
    color = models.CharField(
        max_length=7,
        default='#667eea',
        verbose_name='cor',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='criada em',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='atualizada em',
    )

    class Meta:
        ordering = ['category_type', 'name']
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        unique_together = [['user', 'name']]

    def __str__(self):
        return self.name
