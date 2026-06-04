"""URL configuration for the accounts app.

The `app_name` directive below creates the `accounts:` URL namespace.
Every `reverse_lazy('accounts:account_list')` in `accounts/views.py`
and every `{% url 'accounts:...' %}` in the account templates depends
on this namespace; without it, those reverses raise `NoReverseMatch`.

Mounted in `core/urls.py` at the `/accounts/` prefix, so the four
patterns below resolve to:

  ''                       -> /accounts/                (list)
  'new/'                   -> /accounts/new/            (create)
  '<int:pk>/edit/'         -> /accounts/<pk>/edit/      (update)
  '<int:pk>/delete/'       -> /accounts/<pk>/delete/    (delete)
"""

from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path(
        '',
        views.AccountListView.as_view(),
        name='account_list',
    ),
    path(
        'new/',
        views.AccountCreateView.as_view(),
        name='account_create',
    ),
    path(
        '<int:pk>/edit/',
        views.AccountUpdateView.as_view(),
        name='account_update',
    ),
    path(
        '<int:pk>/delete/',
        views.AccountDeleteView.as_view(),
        name='account_delete',
    ),
]
