# AGENTS.md

Compact, repo-specific guidance for OpenCode sessions in **Finanpy** — a Django 6.0 full-stack personal-finance app. Read this before doing anything non-trivial.

## TL;DR

- Django + DTL + Tailwind (via `django-tailwind`) + SQLite. **No DRF, no SPA, no Celery, no other DB.**
- Class-Based Views only. **Per-user isolation is mandatory** on every authenticated view.
- Work is sequenced in `TASKS.md` (sprint task list). Update it as you complete sub-tasks.
- `tests.py` and Docker are **out of scope until Sprint 5** (PRD RNF-005). Don't create them.

## Setup & commands

The repo ships with `.venv/` and `.env` already in place. Assume the venv is active; if not:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python manage.py tailwind install   # one-time, npm deps for the theme app
python manage.py migrate
python manage.py check              # fast sanity check
```

**Two-process dev loop** (Tailwind needs both):

```bash
python manage.py runserver                # terminal 1
python manage.py tailwind start           # terminal 2 — hot-reloads CSS
```

`python manage.py tailwind build` for a one-shot production CSS build.

**Migrations** — generate per-app, never edit generated files:

```bash
python manage.py makemigrations <app>
python manage.py migrate          # applied per task; do not run in Tarefa 4.1
```

`.env` is **git-ignored** and loaded via `python-decouple`. Required keys: `SECRET_KEY` (mandatory), `DEBUG`, `ALLOWED_HOSTS`, optional `NPM_BIN_PATH`. Never commit secrets.

## Architecture — binding rules

These come from `docs/architecture.md` and `CLAUDE.md` and shape every file. Don't fight them.

- **Custom user by email.** `AUTH_USER_MODEL = 'users.User'` in `core/settings.py`. `username = None`. `USERNAME_FIELD = 'email'`. **No `username` login — ever.**
- **CBVs only.** `TemplateView` / `ListView` / `CreateView` / `UpdateView` / `DeleteView` / `LoginView` / `LogoutView`. No function-based views.
- **Per-user isolation.** Every authenticated view: `LoginRequiredMixin` + `get_queryset` filtered by `self.request.user` (or by a related `account__user`/`category__user` lookup). This is the only thing keeping users from reading each other's data.
- **Balance sync lives ONLY in `transactions/signals.py`** (`post_save`/`post_delete` of `Transaction` updates `Account.balance`). Never mutate `Account.balance` from views, forms, managers, or migrations.
- **Audit fields on every model**, no exceptions: `created_at = models.DateTimeField(auto_now_add=True)` and `updated_at = models.DateTimeField(auto_now=True)`.
- **`on_delete=models.PROTECT`** on FKs to `Account` and `Category` from `Transaction` (financial integrity — never cascade-delete).
- **Money is `DecimalField(max_digits=12, decimal_places=2)`**, rendered with `R$` and the income/expense color rule (`text-emerald-400` / `text-rose-400`).
- **Single SQLite file** at `db.sqlite3` (git-ignored). Do not introduce Postgres or multi-DB.
- **Signals wiring:** `profiles/apps.py` and `transactions/apps.py` override `ready()` to `import <app>.signals`. This is the only place signals get registered.

## URL layout (root: `core/urls.py`)

Independent, non-nested `include`s — don't nest one app's urls under another's:

| Path          | Source             | Notes                                            |
|---------------|--------------------|--------------------------------------------------|
| `/admin/`     | `django.contrib`   | Default admin                                    |
| `/`           | `users.views.HomeView` (name `home`) | Authenticated users are redirected to `dashboard`. |
| `/auth/`      | `users.urls`       | `signup`, `login`, `logout` (public auth forms). |
| `/accounts/`  | `accounts.urls`    | `account_list`/`_create`/`_update/<pk>`/`_delete/<pk>`. |
| `/categories/`| `categories.urls`  | Same CRUD shape as accounts.                     |
| `/dashboard/` | `users.views.DashboardView` (name `dashboard`) | Placeholder until Sprint 5; needed so `LOGIN_REDIRECT_URL` doesn't `NoReverseMatch`. |

`LOGIN_URL = '/auth/login/'`, `LOGIN_REDIRECT_URL = '/'`, `LOGOUT_REDIRECT_URL = '/'` (all in `core/settings.py`).

## Domain apps

| App           | Owns                                                    | Key signals                                  |
|---------------|---------------------------------------------------------|----------------------------------------------|
| `users`       | `User(AbstractUser)` + `UserManager`, `SignupView`/`LoginView`/`LogoutView`/`HomeView`/`DashboardView` | Email-as-username. Login auto-creates user.  |
| `profiles`    | `Profile` (1:1 to `User`)                               | Auto-created via `post_save` signal on `User`. |
| `accounts`    | `Account` FK→User; types `CHECKING`/`SAVINGS`/`WALLET`  | `balance` is **read-only from views**; only signals mutate it. |
| `categories`  | `Category` FK→User; types `INCOME`/`EXPENSE`            | User gets a default set on creation (Sprint 3). |
| `transactions`| `Transaction` FK→`Account` (PROTECT) + FK→`Category` (PROTECT) | **Balance-sync signals live here.** Tarefa 4.1 = model, 4.2 = signals. |

`core/` is the Django project: `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`. `theme/` is auto-generated by `django-tailwind init` — don't hand-edit it.

## Code style

- **Identifiers in English**, **UI strings in pt-BR** (`verbose_name`, labels, error messages, placeholders). They do **not** mix.
- **Single quotes** for all Python strings and DTL attribute values. Double quotes only when the string contains a single quote (e.g. docstrings).
- PEP 8 strictly: 4-space indent, imports ordered stdlib → third-party → local with a blank line between groups.
- `LANGUAGE_CODE = 'pt-br'`, `TIME_ZONE = 'America/Sao_Paulo'`, `USE_I18N = True`, `USE_TZ = True` (set in `core/settings.py`).
- Zero comments unless something is genuinely non-obvious — and module-level docstrings on each `models.py` are required and follow the same style as `accounts/models.py` and `categories/models.py`.
- `related_name` on every FK is explicit and descriptive (e.g. `related_name='transactions'`).

## Subagents — read this first

The project has **three** directories that look like agent folders, only one of which works in OpenCode:

| Path                              | Status in OpenCode                                                        |
|-----------------------------------|---------------------------------------------------------------------------|
| `agents/` (root)                  | **Stale documentation only.** Older reference specs. Ignore.             |
| `.opencode/agents/`                | **Active OpenCode subagents.** Read these to learn their scope/contracts before delegating. |

Subagent names available to the `Task` tool (must match `subagent_type` exactly):

- `django-backend-specialist` — models, CBVs, signals, auth-by-email, forms, URLs, migrations, settings. Consults Context7 for Django 6.0.x APIs.
- `dtl-tailwind-frontend` — DTL templates and Tailwind UI per `docs/design-system.md`.
- `qa-playwright-validator` — end-to-end functional + visual validation via Playwright MCP (server must be running).
- `explore`, `general` — built-in.

**Infra caveat:** the project-specific subagents sometimes fail to invoke (return `{"Error"}` with no detail). The built-in `explore` and `general` agents are reliable. If a project subagent fails, do the work yourself following its contract (read its `.opencode/agent/*.md` file as the spec) or retry once. Don't burn time debugging the subagent system.

**Orchestrator pattern used here:** split a `TASKS.md` task by sub-task scope. Backend (model/view/signal/form/URL/migration/settings) → `django-backend-specialist`. Frontend (DTL/Tailwind templates) → `dtl-tailwind-frontend`. End-to-end check → `qa-playwright-validator`. Pure model tasks (e.g. Tarefa 4.1) need only the backend agent.

## TASKS.md as contract

`TASKS.md` is the living sprint task list. Sub-tasks are `[ ]` (pending) or `[X]` (done). After completing a sub-task via a subagent, **edit `TASKS.md` in place** to flip the box. When all sub-tasks of a task are done, also mark the `Tarefa X.Y concluída` line `[X]`. Don't run unprompted sub-tasks out of order — sprints are sequenced for a reason (e.g. signals depend on the model existing).

## What not to do

- Don't add tests (`tests.py` content) — Sprint 5.
- Don't add Docker — Sprint 5.
- Don't add Celery, Redis, Postgres, DRF, React, Vue, or any JS framework.
- Don't introduce a light theme or off-palette colors. Palette is in `docs/design-system.md` (`bg-slate-900` / `bg-slate-800/60` shell, `from-violet-600 via-indigo-600 to-cyan-500` brand gradient).
- Don't hand-edit `theme/` (auto-generated by django-tailwind) or migration files once generated.
- Don't reintroduce username login.

## Reference docs (read in this order on a new task)

1. `TASKS.md` — what to do next, with explicit sub-task checkboxes.
2. `PRD.md` — full product spec; sprints live in §13.
3. `docs/architecture.md` — the binding rules above, expanded.
4. `docs/apps.md` — per-app responsibility and expected model fields.
5. `docs/code-style.md` — full style checklist.
6. `docs/design-system.md` — Tailwind palette, components, shell layout.
7. `docs/database.md` — ERD and audit-field convention.
8. The matching `.opencode/agent/*.md` file — for the contract a subagent will follow.

Existing `models.py` files in `accounts/` and `categories/` are the **canonical style reference** — copy their shape (docstring, TextChoices, audit fields, `Meta`, `__str__`, `verbose_name` in pt-BR, single quotes) when adding new models.
