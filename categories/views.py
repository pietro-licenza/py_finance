"""Views for the categories app.

Read-only listing is provided by `CategoryListView`; creation, update
and deletion round out the CRUD set.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CategoryForm
from .models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    """List the authenticated user's categories.

    The queryset is restricted to categories owned by
    `self.request.user`, ordered by `category_type` and then `name` (the
    model's default `Meta.ordering`). Beyond the default `categories`
    context key, the view also exposes `income_categories` and
    `expense_categories` so the template can render two sections
    ("Entradas" and "Saídas") without re-querying or filtering in
    Python.
    """

    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """Return only the categories owned by the logged-in user."""
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Split the user's categories into income and expense sections.

        Reuses a single base queryset filtered by the authenticated
        user, then narrows it with a `category_type` filter so Django
        still issues a single `WHERE` clause per section (no list
        comprehensions in Python). The `Category.CategoryType` enum
        members are used instead of the string literals so the choices
        are the single source of truth.
        """
        context = super().get_context_data(**kwargs)
        user_categories = Category.objects.filter(user=self.request.user)
        context['income_categories'] = user_categories.filter(
            category_type=Category.CategoryType.INCOME,
        )
        context['expense_categories'] = user_categories.filter(
            category_type=Category.CategoryType.EXPENSE,
        )
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Create a new category owned by the logged-in user.

    The form (`CategoryForm`) exposes the editable fields of `Category`
    and excludes the `user` FK plus the audit fields. The view binds
    `form.instance.user` to `self.request.user` inside `form_valid`
    so the resulting `Category` is always owned by the authenticated
    user — this is the CreateView equivalent of filtering `get_queryset`
    on ListView and is what enforces per-user isolation on creation.

    The model's `Meta.unique_together = [['user', 'name']]` constraint
    means a second save with the same name for the same user raises
    `IntegrityError` at the database level. The view translates that
    into a field-level error on the `name` input and re-renders the
    form so the template can display the message next to the field
    instead of bubbling a 500 to the user.
    """

    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    # `categories:category_list` will be wired by Tarefa 3.10 once
    # `categories/urls.py` declares `app_name = 'categories'`. The
    # reverse cannot resolve until that namespace exists; that is
    # expected and will be resolved in the URL wiring task.
    success_url = reverse_lazy('categories:category_list')

    def form_valid(self, form):
        """Bind the new category to the logged-in user and persist it.

        The user assignment is what implements per-user isolation on
        create: the form excludes the `user` field, so without this
        override Django would attempt to save the instance with a NULL
        FK and fail. We set the FK here from `self.request.user`.

        The actual save is wrapped in a `transaction.atomic` block so
        that, if the `unique_together = [['user', 'name']]` constraint
        is violated, the entire write is rolled back cleanly. Catching
        `IntegrityError` outside the atomic block is intentional: the
        Django docs warn against catching database exceptions inside an
        atomic block because that would leave the transaction in a
        broken state and any subsequent query in the same request
        would raise `TransactionManagementError`. By catching it
        outside, we re-render the form with `form.add_error` on the
        `name` field and the request continues normally. The success
        message is enqueued only when the save actually commits.
        """
        form.instance.user = self.request.user
        try:
            with transaction.atomic():
                response = super().form_valid(form)
        except IntegrityError:
            # Duplicate (user, name) — translate the database error
            # into a field-level error so the template renders it next
            # to the `name` input. The atomic block above has already
            # rolled back the failed save, so no partial row exists.
            form.add_error(
                'name',
                'Já existe uma categoria com este nome.',
            )
            messages.error(
                self.request,
                'Já existe uma categoria com este nome.',
            )
            return self.form_invalid(form)
        messages.success(self.request, 'Categoria criada com sucesso.')
        return response

    def form_invalid(self, form):
        """Render the form with errors on a failed save.

        Mirrors Django's default behaviour but is overridden here so
        the duplicate-name case (handled in `form_valid`) flows through
        the same re-render path. We do not enqueue an additional
        messages.error here because the caller is expected to attach
        the user-facing error to the relevant field before delegating.
        """
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Expose a page title for the form template.

        Templates typically render a heading like "Nova categoria";
        exposing it from the view (rather than hard-coding it in the
        template) lets the same `category_form.html` be reused by a
        future `CategoryUpdateView`, which can override the context to
        set a different title.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nova categoria'
        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Edit a category owned by the logged-in user.

    The view reuses `CategoryForm` (same editable fields as create) and
    the same `category_form.html` template. Per-user isolation is
    enforced by overriding `get_queryset` to return only the
    authenticated user's categories: when Django resolves the
    `<int:pk>` from the URL through `SingleObjectMixin.get_object`, a
    foreign pk yields no match and Django raises `Http404`, so a user
    can never reach or mutate another user's category.

    The model's `Meta.unique_together = [['user', 'name']]` constraint
    means a rename that collides with another category owned by the
    same user raises `IntegrityError` at the database level. The view
    mirrors `CategoryCreateView` and translates that into a field-level
    error on the `name` input so the template can display the message
    next to the field instead of bubbling a 500 to the user.
    """

    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    # `categories:category_list` will be wired by Tarefa 3.10 once
    # `categories/urls.py` declares `app_name = 'categories'`. The
    # reverse cannot resolve until that namespace exists; that is
    # expected and will be resolved in the URL wiring task.
    success_url = reverse_lazy('categories:category_list')

    def get_queryset(self):
        """Return only the categories owned by the logged-in user.

        This is what implements per-user isolation on update: a user
        who passes another user's pk in the URL gets a 404 because
        `SingleObjectMixin.get_object` cannot find the object in the
        filtered queryset.
        """
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """Persist the edit and notify the user, guarding the unique name.

        The `user` FK and audit fields are not on the form, so we do
        not need to re-bind the user here — the filtered `get_queryset`
        guarantees the instance already belongs to `self.request.user`,
        and the `updated_at` field is refreshed automatically by
        `auto_now=True`.

        The actual save is wrapped in a `transaction.atomic` block so
        that, if the `unique_together = [['user', 'name']]` constraint
        is violated by a rename that collides with another of the
        user's categories, the entire write is rolled back cleanly.
        Catching `IntegrityError` outside the atomic block is
        intentional: the Django docs warn against catching database
        exceptions inside an atomic block because that would leave
        the transaction in a broken state and any subsequent query
        in the same request would raise `TransactionManagementError`.
        By catching it outside, we re-render the form with
        `form.add_error` on the `name` field and the request continues
        normally. The success message is enqueued only when the save
        actually commits.
        """
        try:
            with transaction.atomic():
                response = super().form_valid(form)
        except IntegrityError:
            # Duplicate (user, name) — translate the database error
            # into a field-level error so the template renders it next
            # to the `name` input. The atomic block above has already
            # rolled back the failed save, so no partial row exists.
            form.add_error(
                'name',
                'Já existe uma categoria com este nome.',
            )
            messages.error(
                self.request,
                'Já existe uma categoria com este nome.',
            )
            return self.form_invalid(form)
        messages.success(self.request, 'Categoria atualizada com sucesso.')
        return response

    def get_context_data(self, **kwargs):
        """Expose a page title for the form template.

        Mirrors `CategoryCreateView` so the same `category_form.html`
        renders the correct heading for each action. The form template
        can read `page_title` to display "Editar categoria" here.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Editar categoria'
        return context


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a category owned by the logged-in user.

    Renders `categories/category_confirm_delete.html` on GET and deletes
    the matched `Category` on POST, then redirects to
    `categories:category_list` (the URL name wired in Tarefa 3.10).

    Per-user isolation is enforced by `get_queryset`: when Django
    resolves the `<int:pk>` from the URL through
    `SingleObjectMixin.get_object`, a foreign pk yields no match and
    Django raises `Http404`, mirroring the behaviour of
    `CategoryUpdateView`. An unauthenticated request is redirected to
    the login page by `LoginRequiredMixin`.

    Note on transaction-related validation
    -------------------------------------
    The rule "cannot delete a category that still has transactions" is
    intentionally NOT enforced here. The `Transaction` model does not
    exist yet (it is introduced in Sprint 4 / Tarefa 4.1) and the
    related balance signals are wired in Tarefa 4.2, so the necessary
    relationship lookup cannot be performed today. Adding a placeholder
    would either reference a model that does not exist or rely on a
    manager that would not catch a delete in the `transactions` app
    later.

    The validation must be re-introduced once the `Transaction` model
    exists (see TASKS.md item 6.1.2 - "Validar que não é possível
    excluir categoria com transações"). The recommended implementation
    is to override `form_valid()` on this view to check
    `self.object.transactions.exists()` and, if any exist, call
    `messages.error(...)` and redirect back to
    `categories:category_list` instead of calling
    `super().form_valid(form)`.
    """

    model = Category
    template_name = 'categories/category_confirm_delete.html'
    # Same caveat as `CategoryCreateView` / `CategoryUpdateView`: the
    # namespace `categories:` is introduced by Tarefa 3.10.
    success_url = reverse_lazy('categories:category_list')

    def get_queryset(self):
        """Return only the categories owned by the logged-in user.

        This is what implements per-user isolation on delete: a user
        who passes another user's pk in the URL gets a 404 because
        `SingleObjectMixin.get_object` cannot find the object in the
        filtered queryset.
        """
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """Delete the category and notify the user.

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
        `get_queryset` (a foreign pk is a 404). The `Transaction`
        model does not exist yet, so there are no related rows to
        cascade or balance-reversal signals to worry about here. If
        the "block delete if has transactions" rule is added later
        (see TASKS.md item 6.1.2), the check should live in this
        method so the message-and-redirect path stays in one place.
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Categoria excluída com sucesso.')
        return response
