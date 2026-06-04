---
name: reference-url-namespaces-categories
description: The `categories:` URL namespace is referenced by the list template and the new form/delete templates, but was unwired in Sprint 3 and only gets resolved in Tarefa 3.10.
metadata:
  type: project
---

The Finanpy categories app uses the URL names `categories:category_list`, `categories:category_create`, `categories:category_update`, and `categories:category_delete`. The list template (`templates/categories/category_list.html`) and the new form/delete templates (Tarefa 3.9) already reference these names via `{% url %}`.

**Why:** Tarefa 3.9 (frontend) was committed before Tarefa 3.10 (URL wiring). The new templates must use the exact `categories:*` names so the whole screen set resolves at once when 3.10 lands — picking any other name (or hardcoding paths) would break the integration.

**How to apply:** When working on categories templates, always reference URLs through `{% url 'categories:<name>' %}` with these exact names. Never hardcode `/categories/...` paths. After 3.10 lands, this memory is obsolete and can be removed.

Related: [[feedback-color-swatch-no-js]]
