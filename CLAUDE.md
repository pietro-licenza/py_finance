# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Finanpy** is a full-stack personal finance management system built with Django (no REST APIs, no JS frameworks). It uses email-based authentication, Django Template Language (DTL) + TailwindCSS for the UI, and SQLite as the only database.

The product is in early implementation — the Django project (`core/`) exists and the five domain apps (`users`, `profiles`, `accounts`, `categories`, `transactions`) are scaffolded and registered in `INSTALLED_APPS`, but their models, views, signals, and templates are mostly empty. Work is sequenced through the Sprints described in `PRD.md` section 13.

## Commands

All commands assume the virtualenv in `.venv/` is active.

```bash
# Environment
source .venv/bin/activate
pip install -r requirements.txt

# Migrations
python manage.py makemigrations <app>
python manage.py migrate

# Run dev server (http://127.0.0.1:8000/)
python manage.py runserver

# Admin user
python manage.py createsuperuser

# Tests (planned for Sprint 5 — modules currently empty)
python manage.py test                  # all
python manage.py test <app>            # one app, e.g. accounts
python manage.py test <app>.tests.<TestCase>.<test_method>   # single test
```

## Architecture (the big picture)

These rules are binding — they shape every file in the repo. Most of them aren't enforceable from a single file; future Claude instances need them up front.

- **Django Full Stack, nothing else.** No DRF, no separate API layer, no React/Vue, no Celery, no Postgres. The full feature set is delivered through DTL templates and Django's class-based views.
- **Class-Based Views only.** Use `TemplateView` / `ListView` / `CreateView` / `UpdateView` / `DeleteView` and the native `LoginView` / `LogoutView`. Don't add function-based views unless there is a written reason to.
- **Per-user isolation is mandatory.** Every authenticated view must use `LoginRequiredMixin` and override `get_queryset` to filter by `self.request.user`. This is the only thing preventing user A from reading/mutating user B's accounts, categories, or transactions.
- **Custom user model authenticated by email.** `users.User` extends `AbstractUser` with `username = None`, a unique `email`, `USERNAME_FIELD = 'email'`, empty `REQUIRED_FIELDS`, and a `UserManager(BaseUserManager)` override. `core/settings.py` must declare `AUTH_USER_MODEL = 'users.User'`. Logging in with a username is not supported and must not be reintroduced.
- **Balance synchronization lives in signals — never in views.** `transactions/signals.py` is the single source of truth for `Account.balance`:
  - `post_save` on a new `Transaction`: add `amount` if `income`, subtract if `expense`.
  - `post_save` on edit: reverse the previous impact, then apply the new one.
  - `post_delete`: reverse the impact.
  Signals are wired through `TransactionsConfig.ready()` in `transactions/apps.py`. The same pattern applies to `profiles/signals.py`, which creates a `Profile` automatically on `post_save` of a new `User` (registered via `ProfilesConfig.ready()`).
- **Audit fields on every model.** Every model must include `created_at = models.DateTimeField(auto_now_add=True)` and `updated_at = models.DateTimeField(auto_now=True)`. No exceptions.
- **Templates and design system are constrained.** A root `templates/` directory holds `base.html` (the shell with the fixed sidebar). All authenticated screens extend it. The visual palette is fixed in `docs/design-system.md` — dark theme (`bg-slate-900` / `bg-slate-800/60`), brand gradient `from-violet-600 via-indigo-600 to-cyan-500`, and the income/expense pairing `text-emerald-400` / `text-rose-400`. Do not introduce off-palette colors or a light theme.
- **Single SQLite file.** `db.sqlite3` at the repo root. Don't add support for another DB engine.

## Domain apps (responsibilities)

- `users` — Custom `User` model + `UserManager`. Email is the login identifier.
- `profiles` — `Profile` (1:1 to `User`), created automatically via signal on user creation. Holds `first_name`, `last_name`.
- `accounts` — `Account` (FK to user): `name`, `account_type` (`checking` / `savings` / `cash`), `balance` (`DecimalField(max_digits=12, decimal_places=2)`). Full CRUD via CBVs.
- `categories` — `Category` (FK to user): `name`, `transaction_type` (`income` / `expense`). Full CRUD via CBVs.
- `transactions` — `Transaction` (FK to `Account` and `Category`): `description`, `amount`, `transaction_type`, `date`. Full CRUD via CBVs. Form dropdowns for `account` and `category` must be filtered by the logged-in user. Owns the balance-sync signals.

`core/` is the Django project itself: `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`.

## Code style (project-wide)

- **Code in English** (variables, classes, files, migrations, commits, comments). **UI in Brazilian Portuguese (pt-BR)** (labels, buttons, error messages, placeholders). These don't mix — Portuguese never leaks into identifiers, English never leaks into the rendered UI.
- **Single quotes everywhere.** Python strings and HTML attribute values inside DTL templates must use `'`. Use `"` only when the syntax forces it (e.g. a string containing `'`, docstrings, JSON literals).
- **PEP8** strictly. 4-space indentation. Imports ordered stdlib → third-party → local.
- **`settings.py` localization** must be `LANGUAGE_CODE = 'pt-br'` and `TIME_ZONE = 'America/Sao_Paulo'`.
- **Money** is `DecimalField(max_digits=12, decimal_places=2)`; values are rendered with `R$` and the income/expense color rule above.

## AI agents

When delegating work, the active sub-agents are in **`.claude/agents/`** (not the root `agents/` folder, which holds an older set of reference specs). The live sub-agents are created via `/agents` and are git-ignored:

- `.claude/agents/django-backend-specialist.md` — models, CBVs, signals, auth-by-email, settings.
- `.claude/agents/dtl-tailwind-frontend.md` — DTL templates and Tailwind UI per the Design System.
- `.claude/agents/qa-playwright-validator.md` — visual + functional end-to-end validation.

Always read the sub-agent file **at `.claude/agents/`** before spawning it. The root `agents/` folder is documentation only.

## Out of scope until Sprint 5

Per the PRD's RNF-005, do not invest effort in these before the consolidation sprint:

- Automated tests (`tests.py` modules across apps).
- Docker / `docker-compose.yml`.

## Reference documents

When in doubt, prefer the existing docs over inference. They are not generic — they encode the project's hard constraints.

- `PRD.md` — full product spec (functional + non-functional requirements, ERD, design system, user stories, sprint plan).
- `docs/README.md` — index of the internal docs.
- `docs/architecture.md` — the binding rules above, expanded.
- `docs/apps.md` — per-app responsibility and expected model fields.
- `docs/database.md` — ERD and audit-field convention.
- `docs/design-system.md` — Tailwind palette, components, and the shell layout.
- `docs/code-style.md` — PEP8, quoting rule, language rule, full checklist.
- `docs/contributing.md` — sprint workflow and the per-task quality checklist.
