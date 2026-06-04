"""Forms for the categories app."""

from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):
    """ModelForm for creating and editing Category instances.

    The `user` FK and the audit fields are intentionally excluded — the
    FK is set by the view from `self.request.user`, and the audit fields
    are managed automatically by Django.
    """

    class Meta:
        model = Category
        fields = ('name', 'category_type', 'color')
        labels = {
            'name': 'Nome',
            'category_type': 'Tipo',
            'color': 'Cor',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': (
                    'w-full px-4 py-2 bg-slate-800/60 border border-slate-700 '
                    'rounded-lg text-slate-100 placeholder-slate-500 '
                    'focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                    'focus:border-indigo-500 transition'
                ),
                'placeholder': 'Ex.: Alimentação',
            }),
            'category_type': forms.Select(attrs={
                'class': (
                    'w-full px-4 py-2 bg-slate-800/60 border border-slate-700 '
                    'rounded-lg text-slate-100 focus:outline-none '
                    'focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 '
                    'transition'
                ),
            }),
            'color': forms.ColorInput(attrs={
                'class': (
                    'h-12 w-20 cursor-pointer bg-slate-800/60 border border-slate-700 '
                    'rounded-lg p-1 focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                    'focus:border-indigo-500 transition'
                ),
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The choices on `category_type` already come from the model's
        # TextChoices with pt-BR labels ("Receita", "Despesa"). We just make
        # sure the empty option reads as a human-friendly prompt.
        self.fields['category_type'].empty_label = 'Selecione o tipo'
