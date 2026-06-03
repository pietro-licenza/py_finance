from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import LoginForm, SignupForm


class SignupView(CreateView):
    """Public signup page that creates a User and logs them in automatically."""

    form_class = SignupForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('home')

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

