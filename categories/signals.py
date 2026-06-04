"""
Signals for the categories app.

Creates a fixed set of default categories for each new User so the
transaction form is usable immediately after signup. The list covers
the most common pt-BR personal-finance buckets (income + expense).
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Category

User = get_user_model()


DEFAULT_CATEGORIES = (
    # Receitas (INCOME) — emerald family
    ('Salário',          Category.CategoryType.INCOME,  '#10b981'),
    ('Freelance',        Category.CategoryType.INCOME,  '#22c55e'),
    ('Investimentos',    Category.CategoryType.INCOME,  '#06b6d4'),
    ('Outros (Receita)', Category.CategoryType.INCOME,  '#84cc16'),
    # Despesas (EXPENSE) — rose family + complements
    ('Alimentação',      Category.CategoryType.EXPENSE, '#f43f5e'),
    ('Transporte',       Category.CategoryType.EXPENSE, '#f97316'),
    ('Moradia',          Category.CategoryType.EXPENSE, '#ef4444'),
    ('Saúde',            Category.CategoryType.EXPENSE, '#ec4899'),
    ('Educação',         Category.CategoryType.EXPENSE, '#a855f7'),
    ('Lazer',            Category.CategoryType.EXPENSE, '#eab308'),
    ('Contas',           Category.CategoryType.EXPENSE, '#dc2626'),
    ('Compras',          Category.CategoryType.EXPENSE, '#f59e0b'),
    ('Outros (Despesa)', Category.CategoryType.EXPENSE, '#6b7280'),
)


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    """Create the default category set whenever a new User is created."""
    if created:
        Category.objects.bulk_create(
            [
                Category(
                    user=instance,
                    name=name,
                    category_type=category_type,
                    color=color,
                )
                for name, category_type, color in DEFAULT_CATEGORIES
            ]
        )
