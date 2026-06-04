"""Views for the categories app.

Read-only listing is provided by `CategoryListView`; creation, update
and deletion round out the CRUD set.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

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
