---
name: bug-008-block-content-wrapper
description: BUG-008 — base.html wraps the parent {% block content %} in a conditional with {{ block.super }} on each branch. Django template inheritance replaces the parent block entirely, so the conditional never runs and {{ block.super }} is irrelevant. Sidebar missing on every page + {# #} comments leak.
metadata:
  type: project
---

The BUG-007 fix in `templates/base.html` is structurally broken. The pattern:

```django
{% block content %}
  {% if user.is_authenticated %}
    <div>{% include 'partials/_sidebar.html' %}<main>{{ block.super }}</main></div>
  {% else %}
    <main>{{ block.super }}</main>
  {% endif %}
{% endblock %}
```

combined with a child template like `dashboard.html`:

```django
{% block content %}
<section>...</section>
{% endblock %}
```

Does NOT work. Django's `{% extends %}` inheritance **replaces** the parent's `{% block content %}` entirely with the child's `{% block content %}`. The parent's `{% if %}` is never evaluated, and the `{{ block.super }}` in the parent's block has no effect (it would refer to the child's content, but the child is the one being rendered directly).

Observed symptoms in the rendered HTML on every page:
- No `<aside>` element (sidebar never included)
- No `<main>` wrapper (the wrapper div never rendered)
- `{# Toasts em body-level ... #}` (and other `{# #}` comments) appearing as raw text in the body — Django's `{# #}` comment stripping happens during template parsing, but if the template inheritance is broken, the body is rendered with the raw `{% if %}` block not being processed, leaving the comments in the output.

**Why this is not caught by Django's template engine:** Django doesn't raise an error for "dead code" inside a parent block that's overridden by a child. The unused `{% if %}` and `{{ block.super }}` are just silently ignored.

**How to apply:** If a QA session sees `{# #}` text in the browser or no `<aside>` on authenticated pages, the root cause is the `{% block %}` wrapper pattern in `base.html`. Quick diagnosis: `curl -s http://127.0.0.1:8000/dashboard/ | grep -c '{#'` returns > 0 = bug present. Returns 0 = `{# #}` stripping is working normally.

The fix needs to use a different pattern: either move the shell into a `{% block sidebar %}` that children don't need to define, or skip the parent block entirely and have children emit the shell themselves.
