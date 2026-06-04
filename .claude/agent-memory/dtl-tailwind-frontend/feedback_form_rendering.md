---
name: form-rendering-pattern
description: Canonical DTL pattern for rendering ModelForm fields in Finanpy templates — when to use manual per-field rendering vs form.as_p
metadata:
  type: feedback
---

For ModelForm-backed CRUD forms in Finanpy, render each field manually with `<label for='{{ form.field.id_for_label }}'>{{ form.field.label }}</label>` followed by `{{ form.field }}`, `{{ form.field.help_text }}`, and `{{ form.field.errors }}`. Never use `{{ form.as_p }}`.

**Why:** The project's `AccountForm` (and `CategoryForm`, `TransactionForm` later) define widget classes per-field in `forms.py` Meta.widgets. Rendering fields manually with a styled `<label>` + the auto-styled widget gives full control over label typography (`block text-sm font-medium text-slate-300 mb-1.5`) and produces a consistent dark-themed form. `{{ form.as_p }}` would lose the styled label and wrap everything in Django's default `<p>` containers that don't match the design system.

**How to apply:** Use this pattern for every CRUD form template (account_form, category_form, transaction_form). The exact div-wrapping for each field is: `<div class='space-y-1.5'>` (or `space-y-1` if tighter) containing a styled `<label>`, the `{{ form.field }}` (widget classes already applied in the form), an optional `<p class='text-xs text-slate-500'>` for help_text, and a `<p class='text-rose-400 text-sm mt-1'>` for errors. Always include `{{ form.non_field_errors }}` at the top of the `<form>` inside a `bg-rose-500/10 border border-rose-500/30 text-rose-300` container for top-level form errors. Add `novalidate` to the form tag to keep browser validation off — Django's server-side validation is the source of truth.

Related: [[design-system-palette]], [[cancel-button-as-anchor]]
