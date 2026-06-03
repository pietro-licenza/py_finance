"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # The public landing page is the project root; authenticated visitors are
    # bounced to the dashboard (5.1) by HomeView.get.
    path('', users_views.HomeView.as_view(), name='home'),
    # The auth namespace lives under /auth/ for clear grouping of public pages
    # (login, signup, logout) and to make room for other public pages at the root.
    path('auth/', include('users.urls')),
    # The dashboard lives at the project root, not under /auth/, because it is
    # an authenticated destination, not a public auth form. Full dashboard is
    # built in Sprint 5; the placeholder keeps the post-login redirect chain
    # (HomeView -> 'dashboard') from breaking with NoReverseMatch in Sprint 1.
    path('dashboard/', users_views.DashboardView.as_view(), name='dashboard'),
]
