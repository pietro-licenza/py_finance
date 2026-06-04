"""Views for the accounts app.

Read-only listing is provided by `AccountListView`; creation, update
and deletion are scheduled for later sprints.
"""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import AccountForm
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


class AccountCreateView(LoginRequiredMixin, CreateView):
    """Create a new account owned by the logged-in user.

    The form (`AccountForm`) exposes the editable fields of `Account`
    and excludes the `user` FK plus the audit fields. The view binds
    `form.instance.user` to `self.request.user` inside `form_valid`
    so the resulting `Account` is always owned by the authenticated
    user — this is the CreateView equivalent of filtering `get_queryset`
    on ListView and is what enforces per-user isolation on creation.
    """

    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    # `accounts:account_list` will be wired by Tarefa 2.11 once
    # `accounts/urls.py` declares `app_name = 'accounts'`. The reverse
    # cannot resolve until that namespace exists; that is expected and
    # will be resolved in the URL wiring task.
    success_url = reverse_lazy('accounts:account_list')

    def form_valid(self, form):
        """Bind the new account to the logged-in user and notify them.

        The user assignment is what implements per-user isolation on
        create: the form excludes the `user` field, so without this
        override Django would attempt to save the instance with a NULL
        FK and fail. We set the FK here from `self.request.user`,
        persist via `super().form_valid`, then enqueue a success
        message that the template will render through the messages
        framework.
        """
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Conta criada com sucesso.')
        return response

    def get_context_data(self, **kwargs):
        """Expose a page title for the form template.

        Templates typically render a heading like "Nova conta"; exposing
        it from the view (rather than hard-coding it in the template)
        lets the same `account_form.html` be reused by `AccountUpdateView`
        in a later sprint, which can override the context to set a
        different title.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nova conta'
        return context
