from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm


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
