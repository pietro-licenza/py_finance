"""Forms for the accounts app."""

from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    """ModelForm for creating and editing Account instances.

    The `user` FK and the audit fields are intentionally excluded — the
    FK is set by the view from `self.request.user`, and the audit fields
    are managed automatically by Django.
    """

    class Meta:
        model = Account
        fields = ('name', 'bank_name', 'account_type', 'balance')
        labels = {
            'name': 'Nome',
            'bank_name': 'Banco',
            'account_type': 'Tipo de conta',
            'balance': 'Saldo inicial',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': (
                    'w-full px-4 py-2 bg-slate-800/60 border border-slate-700 '
                    'rounded-lg text-slate-100 placeholder-slate-500 '
                    'focus:outline-none focus:ring-2 focus:ring-violet-500 '
                    'focus:border-transparent transition'
                ),
                'placeholder': 'Ex.: Conta principal',
            }),
            'bank_name': forms.TextInput(attrs={
                'class': (
                    'w-full px-4 py-2 bg-slate-800/60 border border-slate-700 '
                    'rounded-lg text-slate-100 placeholder-slate-500 '
                    'focus:outline-none focus:ring-2 focus:ring-violet-500 '
                    'focus:border-transparent transition'
                ),
                'placeholder': 'Ex.: Nubank, Itaú, Carteira...',
            }),
            'account_type': forms.Select(attrs={
                'class': (
                    'w-full px-4 py-2 bg-slate-800/60 border border-slate-700 '
                    'rounded-lg text-slate-100 focus:outline-none '
                    'focus:ring-2 focus:ring-violet-500 focus:border-transparent '
                    'transition'
                ),
            }),
            'balance': forms.NumberInput(attrs={
                'class': (
                    'w-full px-4 py-2 bg-slate-800/60 border border-slate-700 '
                    'rounded-lg text-slate-100 placeholder-slate-500 '
                    'focus:outline-none focus:ring-2 focus:ring-violet-500 '
                    'focus:border-transparent transition'
                ),
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The choices on `account_type` already come from the model's
        # TextChoices with pt-BR labels ("Conta Corrente", "Conta Poupança",
        # "Carteira"). We just make sure the empty option reads as a
        # human-friendly prompt.
        self.fields['account_type'].empty_label = 'Selecione o tipo de conta'
