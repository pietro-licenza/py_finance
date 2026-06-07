"""
Transaction model for the Finanpy project.

Represents a single financial movement (income or expense) posted
against a user's account and tagged with a user-defined category.
The `Account.balance` is kept in sync with these rows exclusively by
`transactions/signals.py` -- never mutate it from views, forms, or
migrations.
"""

from django.db import models

from accounts.models import Account
from categories.models import Category


class Transaction(models.Model):
    """A single income or expense posted against an account."""

    class TransactionType(models.TextChoices):
        INCOME = 'INCOME', 'Receita'
        EXPENSE = 'EXPENSE', 'Despesa'

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='conta',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='categoria',
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        verbose_name='tipo',
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='valor',
    )
    transaction_date = models.DateField(
        verbose_name='data',
    )
    description = models.TextField(
        blank=True,
        verbose_name='descrição',
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
        ordering = ['-transaction_date', '-id']
        verbose_name = 'transação'
        verbose_name_plural = 'transações'
        indexes = [
            models.Index(fields=['account', 'transaction_date']),
            models.Index(fields=['category', 'transaction_date']),
        ]

    def __str__(self):
        if self.description:
            return f'{self.transaction_date} - {self.description[:30]}'
        return f'{self.transaction_date} - {self.category}'
