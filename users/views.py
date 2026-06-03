from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import LoginForm, SignupForm


class SignupView(CreateView):
    """Public signup page that creates a User and logs them in automatically."""

    form_class = SignupForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Conta criada com sucesso. Bem-vindo ao Finanpy!')
        return response


class LoginView(FormView):
    """Public login page that authenticates a User via email + password."""

    form_class = LoginForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, email=email, password=password)
        if user is None:
            form.add_error(None, 'E-mail ou senha inválidos.')
            messages.error(self.request, 'Credenciais inválidas. Verifique e tente novamente.')
            return self.form_invalid(form)

        login(self.request, user)
        messages.success(self.request, f'Bem-vindo de volta, {user.email}!')
        return super().form_valid(form)


class LogoutView(LogoutView):
    """Logout that flashes a friendly message before signing the user out.

    Wraps Django's built-in LogoutView to inject a success message into the
    session before the user is signed out — the message will then be rendered
    on the page the user is redirected to (LOGOUT_REDIRECT_URL).
    """

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Você saiu da sua conta. Até logo!')
        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    """Public landing page shown to unauthenticated visitors.

    Authenticated users are bounced to the dashboard so the marketing page
    is only ever shown to people who haven't signed up yet.
    """

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Sprint 1 placeholder for the authenticated landing page.

    The full dashboard (accounts overview, recent transactions, charts, etc.)
    is delivered in Sprint 5. For now this view authenticates the user and
    renders a friendly "welcome" page so the post-login / post-signup redirect
    chain (HomeView -> dashboard) terminates on a real, styled page instead
    of breaking with NoReverseMatch.
    """

    template_name = 'dashboard.html'

