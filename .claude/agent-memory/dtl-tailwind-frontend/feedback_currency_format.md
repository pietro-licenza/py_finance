---
name: feedback-currency-format
description: Render BRL monetary values with `R$ {{ value|floatformat:'2g' }}` — built-in filter, no humanize dependency, no custom filter
metadata:
  type: feedback
---

Always render monetary values with `R$ {{ value|floatformat:'2g' }}`.

**Why:** Django 6's `floatformat` accepts a `'g'` suffix that forces locale-aware grouping. With `LANGUAGE_CODE = 'pt-br'` (already in `core/settings.py`), `1234.5` becomes `1.234,50` — exactly the pt-BR convention the Design System requires (`R$ 1.234,56`). The `'2'` enforces two decimal places even when the value is whole (`100` -> `100,00`). Source: Django 6.0 docs, "floatformat" — the `'g'` suffix explicitly enables locale-specific grouping; `'u'` would disable localization.

**How to apply:** Use on every monetary value in every template (account balance, total balance, transaction amount, dashboard totals). Do NOT use `humanize`/`intcomma` — `django.contrib.humanize` is not in `INSTALLED_APPS` and adding it just for this is wasteful. Do NOT wait for a custom currency filter (planned for Tarefa 5.7) — the built-in handles every case the project needs. Pair with the income/expense color rule: `text-emerald-400` for receitas, `text-rose-400` for despesas / negative balances; neutral `text-slate-100` / `text-white` for non-signed balances.

Quoting note inside templates: `floatformat:'2g'` uses single quotes because the project rule is single quotes in HTML attributes and DTL string args.

Related: [[feedback-design-system-palette]] for the color tokens this pairs with.
