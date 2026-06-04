---
name: project-state-sprint-3-qa
description: Sprint 3 (Categorias) QA E2E completed on 2026-06-04 — 2 bugs found (V-07 missing sidebar, V-10 wrong/missing focus ring). 10/10 functional subtasks PASS. Test user left for cleanup.
metadata:
  type: project
---

Sprint 3 Categories E2E QA executed 2026-06-04 against the live Django server (http://127.0.0.1:8000/, just confirmed responding). All 10 Tarefa 3.13 subtasks executed end-to-end.

**Functional (F-13.1 to F-13.10): 10/10 PASS**
- Signup of a fresh user triggered the Tarefa 3.12 signal — 13 default categories (4 INCOME + 9 EXPENSE) appeared immediately.
- Create / Edit / Delete for custom income and expense categories worked, with PT-BR success messages and per-category custom color preserved (inline style on `<article>`).
- Duplicate name correctly re-renders the form with "Já existe uma categoria com este nome." inline (styled `text-rose-400 text-sm mt-1`).
- Color picker is the native browser `<input type="color">` — works as pre-filler on Edit.

**Visual (V-13): 2 FAILs**
- **V-07 FAIL — Sidebar shell missing on /categories/**: The body contains only `<main class="min-h-screen">` — no `<aside>`, no `bg-slate-950` shell wrapper, no fixed left nav with Dashboard/Contas/Categorias/Transações links. `docs/design-system.md` lines 88-115 mandate this shell on every authenticated screen. This is a structural regression on Tarefa 3.7 (templates).
- **V-10 FAIL — Input focus ring is wrong color**: The template uses `focus:ring-violet-500` (and the design system spec actually says `focus:ring-indigo-500` at line 83), but the computed focus ring color is `rgb(37, 99, 235)` = `blue-600` (Tailwind's default ring color) — proving the **violet-500 / indigo-500 ring utilities are missing from the compiled Tailwind bundle**. `from-violet-600` and `from-indigo-600` ARE present (Salvar button gradient works), so the missing class is specifically `ring-violet-500` / `ring-indigo-500`. Likely a `content` paths / safelist issue in `tailwind.config.js` — see [[feedback-tailwind-bundle-check]].

**Other visual checks (PT-BR / dark theme / Entradas-Saídas color split / mobile): all PASS**
- V-01: `bg-slate-900` ✓ (body bg = rgb(15, 23, 42))
- V-08: zero English text found via regex
- V-09: at 375x812 no horizontal overflow on the list or create form
- V-13: Entradas = `text-emerald-400` (rgb(52, 211, 153)); Saídas = `text-rose-400` (rgb(251, 113, 133))

**Test user (left in DB for cleanup):**
- email: `sprint3-qa-1780581220@finanpy.com`
- password: `QASprint3Pass!2026`
- default categories populated by Tarefa 3.12 signal
- user added 1 custom income (Comissões → renamed to "Comissões e Bônus" in F-13.7) and 1 custom expense (Pet Shop, deleted in F-13.9)

**Why:** the next round of sprint work needs the sidebar + Tailwind ring issues fixed before Sprint 4 (Transactions) reuses the same shell.

**How to apply:** if a future Sprint 4 QA session re-encounters missing sidebar or wrong focus ring on /transactions/ or /accounts/, it's the same root cause (Sprint 3 templates/templates-base), not a new bug.
