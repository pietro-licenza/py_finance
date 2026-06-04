"""URL configuration for the categories app.

The `app_name` directive below creates the `categories:` URL namespace.
Every `reverse_lazy('categories:...')` in `categories/views.py` and
every `{% url 'categories:...' %}` in the category templates depends
on this namespace; without it, those reverses raise `NoReverseMatch`.

Mounted in `core/urls.py` at the `/categories/` prefix, so the four
patterns below resolve to:

  ''                       -> /categories/                (list)
  'new/'                   -> /categories/new/            (create)
  '<int:pk>/edit/'         -> /categories/<pk>/edit/      (update)
  '<int:pk>/delete/'       -> /categories/<pk>/delete/    (delete)
"""

from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path(
        '',
        views.CategoryListView.as_view(),
        name='category_list',
    ),
    path(
        'new/',
        views.CategoryCreateView.as_view(),
        name='category_create',
    ),
    path(
        '<int:pk>/edit/',
        views.CategoryUpdateView.as_view(),
        name='category_update',
    ),
    path(
        '<int:pk>/delete/',
        views.CategoryDeleteView.as_view(),
        name='category_delete',
    ),
]
