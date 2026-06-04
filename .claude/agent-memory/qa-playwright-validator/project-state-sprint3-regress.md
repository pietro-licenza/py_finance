---
name: project-state-sprint3-regress
description: Sprint 3 regression QA on 2026-06-04 — BUG-005 fix is BROKEN (BUG-008). Sidebar missing, no <main> wrapper, {# #} comments leak into HTML on EVERY page. BUG-006 (focus ring) PASSES.
metadata:
  type: project
---

Sprint 3 regression QA executed 2026-06-04. The BUG-005 fix (sidebar shell) and the BUG-007 follow-up fix (block content wrapper) are both broken. BUG-006 fix is solid.

**BUG-005 fix is BROKEN (P0) — see [[bug-008-block-content-wrapper]]**
On every page that extends `base.html` (dashboard, categories, accounts, login, signup, landing), the rendered HTML has:
- NO `<aside>` sidebar (only the dashboard's H1/Sair from the inner section are visible)
- NO `<main>` wrapper
- Django `{# #}` comments LEAK into the HTML body as raw text (visible in browser as literal `{# Toasts em body-level ... #}` at the top of every page)

Root cause: `base.html` lines 44-64 wrap the conditional inside `{% block content %}` and use `{{ block.super }}` in each branch. But Django template inheritance **replaces** the parent block entirely with the child block — the parent's `{% if %}` is never evaluated, and `{{ block.super }}` is moot. The whole pattern is fundamentally incompatible with how `{% block %}` works in child-extending templates.

**BUG-006 fix PASSES (P1 closed)**
On `/categories/new/`:
- Nome input: `box-shadow` = `rgb(255, 255, 255) 0px 0px 0px 0px, rgb(99, 102, 241) 0px 0px 0px 2px, rgba(0, 0, 0, 0) 0px 0px 0px 0px` → indigo-500 confirmed
- Tipo select: same
- Cor color input: same
- `border-color` = `rgb(99, 102, 241)` on focus
- No blue-600 fallback, no violet-500 leak. The safelist + recompile worked.

**F-13.x smoke (10 scenarios) — 5/10 PASS (only the ones that don't depend on the sidebar shell)**
- F-13.3 PASS: signup of fresh user triggered the Tarefa 3.12 signal — 13 default categories (4 INCOME + 9 EXPENSE) appeared immediately.
- F-13.4 PASS: custom income "Comissões e Bônus" created.
- F-13.5 PASS: custom expense "Pet Shop" created (15 total articles).
- F-13.8 PASS: duplicate name "Salário" re-renders the form with "Já existe uma categoria com este nome." inline.
- F-13.9 PASS: delete confirmation flow works, "Pet Shop" removed, back to 14.
- F-13.10 PASS: Entradas = `text-emerald-400` (rgb 52, 211, 153); Saídas = `text-rose-400` (rgb 251, 113, 133).

**F-13.x NOT executed (depend on sidebar)**
- F-13.1, F-13.2, F-13.6, F-13.7 — all reference "click sidebar link" / "active sidebar item" / "sidebar reflects current page" — N/A because there is no sidebar.

**Public pages — no 500s, but BROKEN LAYOUT**
- `/` landing: renders marketing content (Criar Conta, Já tenho conta), NO sidebar (correct), but NO `<main>` and `{# #}` comment leaks.
- `/auth/login/`: renders Entrar form, no sidebar (correct), but NO `<main>` and `{# #}` leak.
- `/auth/signup/`: renders Criar Conta form, no sidebar (correct), but NO `<main>` and `{# #}` leak.

**Test user (left in DB)**
- email: `sprint3-regress-1780584443@finanpy.com`
- password: `QARegress2026!Pass`
- 13 default categories populated
- 1 custom income: "Comissões e Bônus"
- "Pet Shop" was created then deleted in F-13.9

**Why:** BUG-007 was meant to be a quick fix for "block tag appears more than once" — the developer's `{{ block.super }}` inside the parent block is a Django template inheritance pattern that does not work the way it does in non-block contexts. Need to either (a) move the sidebar into a separate `{% block sidebar %}` that child templates don't need to touch, or (b) stop using `{% block content %}` in `base.html` entirely and let the child templates emit their own shell.

**How to apply:** if a future Sprint 4 / Sprint 5 QA session re-encounters `{# #}` text in the browser or no sidebar anywhere, the diagnosis is the same root cause in `base.html`. Quick check: `curl -s http://127.0.0.1:8000/dashboard/ | grep -c '{#'` should return 0 for healthy code.
