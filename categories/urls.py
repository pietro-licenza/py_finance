"""TEMPORARY URL config for the categories app (QA stub for Tarefa 3.5).

This file exists ONLY to let `templates/categories/category_list.html`
render during the QA validation of Tarefa 3.5. The template references
four named URLs — `category_list`, `category_create`, `category_update`
and `category_delete` — that the official Tarefa 3.10 will register.

Until 3.10 lands, the three CRUD endpoints (`create`, `update`,
`delete`) point at a stub view that returns HTTP 501. This keeps the
`{% url %}` tags resolvable so the list page renders, but anyone who
clicks one of those buttons gets a clear "not implemented yet" response
instead of a misleading 404 or a NoReverseMatch crash.

Tarefa 3.10 must REPLACE this file with the real CRUD wiring.
"""

from django.http import HttpResponse
from django.urls import path

from .views import CategoryListView


def _not_implemented(request, *args, **kwargs):
    """Stub for CRUD endpoints that Tarefa 3.10 will implement."""
    return HttpResponse(
        'Esta rota ainda não foi implementada (Tarefa 3.10).',
        status=501,
    )


app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('new/', _not_implemented, name='category_create'),
    path('<int:pk>/edit/', _not_implemented, name='category_update'),
    path('<int:pk>/delete/', _not_implemented, name='category_delete'),
]
