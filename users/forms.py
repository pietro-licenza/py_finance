from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

INPUT_CLASSES = (
    'block w-full px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg '
    'text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 '
    'focus:ring-indigo-500 focus:border-indigo-500 text-sm transition-colors '
    'duration-150'
)


class SignupForm(UserCreationForm):
    """Signup form for the custom email-based User model."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'seu@email.com',
            'autocomplete': 'email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'Crie uma senha',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'Confirme sua senha',
            'autocomplete': 'new-password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe um usuário cadastrado com este e-mail.')
        return email


class LoginForm(forms.Form):
    """Login form for the custom email-based User model."""

    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'seu@email.com',
            'autocomplete': 'email',
        })
        self.fields['password'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'Sua senha',
            'autocomplete': 'current-password',
        })
