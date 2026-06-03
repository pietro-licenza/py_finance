from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # Note: the 'dashboard' URL is mounted at /dashboard/ directly in
    # core/urls.py (not under /auth/) because the dashboard is an
    # authenticated destination, not part of the public auth namespace.
]
