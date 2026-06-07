"""
Balance-sync signals for the Finanpy project.

Whenever a Transaction is created, updated, or deleted, the related
Account.balance is kept in sync automatically. This is the only
place where Account.balance should be mutated — never from views,
forms, or migrations.
"""

from django.db.models import F
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from accounts.models import Account
from .models import Transaction


def _transaction_impact(transaction):
    """Return the signed amount a transaction adds to its account."""
    if transaction.transaction_type == Transaction.TransactionType.INCOME:
        return transaction.amount
    return -transaction.amount


@receiver(post_save, sender=Transaction)
def update_balance_on_create(sender, instance, created, **kwargs):
    """Add the transaction impact to the account when a new row is created."""
    if not created:
        return
    Account.objects.filter(pk=instance.account_id).update(
        balance=F('balance') + _transaction_impact(instance),
    )


@receiver(post_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    """Reverse the transaction impact when a row is deleted."""
    Account.objects.filter(pk=instance.account_id).update(
        balance=F('balance') - _transaction_impact(instance),
    )


@receiver(pre_save, sender=Transaction)
def update_balance_on_update(sender, instance, **kwargs):
    """Adjust account balances when an existing transaction is changed.

    On update we must reverse the old impact and apply the new one.
    If the account changed we touch both the old and the new account.
    """
    if not instance.pk:
        return
    try:
        old = Transaction.objects.get(pk=instance.pk)
    except Transaction.DoesNotExist:
        return

    old_impact = _transaction_impact(old)
    new_impact = _transaction_impact(instance)

    if old.account_id == instance.account_id:
        Account.objects.filter(pk=instance.account_id).update(
            balance=F('balance') + (new_impact - old_impact),
        )
    else:
        Account.objects.filter(pk=old.account_id).update(
            balance=F('balance') - old_impact,
        )
        Account.objects.filter(pk=instance.account_id).update(
            balance=F('balance') + new_impact,
        )