"""Views for the accounts app.

Read-only listing is provided by `AccountListView`; creation, update
and deletion are scheduled for later sprints.
"""

from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import ListView

from .models import Account


class AccountListView(LoginRequiredMixin, ListView):
    """List the authenticated user's accounts.

    The queryset is restricted to accounts owned by `self.request.user`,
    ordered by `name` (the model's default `Meta.ordering`). The total
    balance across the user's active accounts is exposed in the context
    as `total_balance` so the template can render a single headline
    figure without re-aggregating.
    """

    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        """Return only the accounts owned by the logged-in user."""
        return Account.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add the aggregated total balance for the user's accounts.

        `Sum` with `default=Decimal('0')` keeps the template safe when
        the user has no accounts yet, avoiding a `None` that would
        break numeric formatting.
        """
        context = super().get_context_data(**kwargs)
        total = Account.objects.filter(
            user=self.request.user,
        ).aggregate(total=Sum('balance', default=Decimal('0')))['total']
        context['total_balance'] = total
        return context
