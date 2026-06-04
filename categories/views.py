"""Views for the categories app.

Read-only listing is provided by `CategoryListView`; creation, update
and deletion round out the CRUD set.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

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
