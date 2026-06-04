"""Views for the accounts app.

Read-only listing is provided by `AccountListView`; creation, update
and deletion round out the CRUD set.
"""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

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


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an account owned by the logged-in user.

    The view reuses `AccountForm` (same editable fields as create) and
    the same `account_form.html` template. Per-user isolation is
    enforced by overriding `get_queryset` to return only the
    authenticated user's accounts: when Django resolves the `<int:pk>`
    from the URL through `SingleObjectMixin.get_object`, a foreign pk
    yields no match and Django raises `Http404`, so a user can never
    reach or mutate another user's account.
    """

    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    # Same caveat as `AccountCreateView`: the namespace `accounts:` is
    # introduced by Tarefa 2.11.
    success_url = reverse_lazy('accounts:account_list')

    def get_queryset(self):
        """Return only the accounts owned by the logged-in user.

        This is what implements per-user isolation on update: a user
        who passes another user's pk in the URL gets a 404 because
        `SingleObjectMixin.get_object` cannot find the object in the
        filtered queryset.
        """
        return Account.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """Persist the edit and notify the user.

        The `user` FK and audit fields are not on the form, so we do
        not need to re-bind the user here — the filtered `get_queryset`
        guarantees the instance already belongs to `self.request.user`,
        and the `updated_at` field is refreshed automatically by
        `auto_now=True`. The `balance` field is editable on this form
        because it represents the account's own opening/edited balance,
        not a transaction effect; balance changes driven by
        transactions are applied exclusively in
        `transactions/signals.py`.
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Conta atualizada com sucesso.')
        return response

    def get_context_data(self, **kwargs):
        """Expose a page title for the form template.

        Mirrors `AccountCreateView` so the same `account_form.html`
        renders the correct heading for each action. The form template
        can read `page_title` to display "Editar conta" here.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Editar conta'
        return context


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an account owned by the logged-in user.

    Renders `accounts/account_confirm_delete.html` on GET and deletes
    the matched `Account` on POST, then redirects to
    `accounts:account_list` (the URL name wired in Tarefa 2.11).

    Per-user isolation is enforced by `get_queryset`: when Django
    resolves the `<int:pk>` from the URL through
    `SingleObjectMixin.get_object`, a foreign pk yields no match and
    Django raises `Http404`, mirroring the behaviour of
    `AccountUpdateView`. An unauthenticated request is redirected to
    the login page by `LoginRequiredMixin`.

    Note on transaction-related validation
    -------------------------------------
    The rule "cannot delete an account that still has transactions" is
    intentionally NOT enforced here. The `Transaction` model does not
    exist yet (it is introduced in Sprint 4) and the related balance
    signals are wired in Tarefa 4.2, so the necessary relationship
    lookup cannot be performed today. Adding a placeholder would
    either reference a model that does not exist or rely on a manager
    that would not catch a delete in the `transactions` app later.

    The validation must be re-introduced once the `Transaction` model
    exists (see TASKS.md item 6.1.1 - "Validar que não é possível
    excluir conta com transações"). The recommended implementation
    is to override `form_valid()` on this view to check
    `self.object.transactions.exists()` and, if any exist, call
    `messages.error(...)` and redirect back to `accounts:account_list`
    instead of calling `super().form_valid(form)`.
    """

    model = Account
    template_name = 'accounts/account_confirm_delete.html'
    # Same caveat as `AccountCreateView` / `AccountUpdateView`: the
    # namespace `accounts:` is introduced by Tarefa 2.11.
    success_url = reverse_lazy('accounts:account_list')

    def get_queryset(self):
        """Return only the accounts owned by the logged-in user.

        This is what implements per-user isolation on delete: a user
        who passes another user's pk in the URL gets a 404 because
        `SingleObjectMixin.get_object` cannot find the object in the
        filtered queryset.
        """
        return Account.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """Delete the account and notify the user.

        In Django 4.0+ `BaseDeleteView.post` inlines the form-handling
        flow (set `self.object`, build a `Form`, validate, dispatch)
        and calls `self.form_valid(form)` on success — it does NOT
        delegate to `DeletionMixin.delete()` as older Django releases
        did. `form_valid` is therefore the correct hook to enrich the
        delete pipeline: `super().form_valid(form)` performs the
        actual `self.object.delete()` and returns the redirect, and
        we enqueue the success message before returning that same
        response so `MessageMiddleware.process_response` persists it
        for the next request to render. The user is bound through
        `get_queryset` (a foreign pk is a 404), and balance sync is
        unaffected: deletion of an `Account` does not mutate any
        other account's balance, and the `Transaction` model does not
        exist yet, so there are no balance-reversal signals to worry
        about here. If the "block delete if has transactions" rule is
        added later, the check should live in this method so the
        message-and-redirect path stays in one place.
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Conta excluída com sucesso.')
        return response
