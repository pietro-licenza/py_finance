"""
Account model for the Finanpy project.

Represents a bank account owned by a user. The `balance` field is the
authoritative source of the account's current value and is updated
exclusively by `transactions/signals.py` whenever a Transaction is
created, updated, or deleted.
"""

from django.conf import settings
from django.db import models


class Account(models.Model):
    """A user's bank account (checking, savings, or wallet)."""

    class AccountType(models.TextChoices):
        CHECKING = 'CHECKING', 'Conta Corrente'
        SAVINGS = 'SAVINGS', 'Conta Poupança'
        WALLET = 'WALLET', 'Carteira'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='usuário',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='nome',
    )
    bank_name = models.CharField(
        max_length=100,
        verbose_name='nome do banco',
    )
    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.CHECKING,
        verbose_name='tipo de conta',
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='saldo',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='ativa',
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
        ordering = ['name']
        verbose_name = 'conta'
        verbose_name_plural = 'contas'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['user', 'account_type']),
        ]

    def __str__(self):
        return self.name
