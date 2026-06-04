---
name: deleteview-form-valid-not-delete
description: In Django 4.0+ (incl. 6.0.5) generic DeleteView dispatches POST through form_valid, not delete — override form_valid to add side effects like messages.
metadata:
  type: feedback
---

When subclassing `django.views.generic.DeleteView` on Django 4.0+ (this project runs 6.0.5), override `form_valid(self, form)` — NOT `delete(self, request, *args, **kwargs)` — to add side effects such as `messages.success(...)`, audit logging, or pre-delete validation that should block the deletion and redirect with a message.

**Why:** `BaseDeleteView.post` (in `django/views/generic/edit.py`) inlines the form-handling flow and explicitly calls `self.form_valid(form)` on success. It does NOT delegate to `DeletionMixin.delete()` the way pre-4.0 releases did. An override of `delete()` therefore becomes dead code that fails silently — the deletion still happens (because `BaseDeleteView.form_valid` runs `self.object.delete()`), the user is still redirected, but anything added in `delete()` (messages, logging, audit hooks) never executes. This bit BUG-001 in Sprint 2: the delete success toast never appeared because the `delete()` override on `AccountDeleteView` was never invoked.

**How to apply:**
- For a success message after a successful delete:
  ```python
  def form_valid(self, form):
      response = super().form_valid(form)
      messages.success(self.request, 'Conta excluída com sucesso.')
      return response
  ```
- To block the delete (e.g. "cannot delete an account that still has transactions"), check on `self.object` before `super().form_valid(form)` and return `HttpResponseRedirect(self.get_success_url())` with a `messages.error(...)` instead of calling super.
- `messages` added before returning the redirect response are persisted by `MessageMiddleware.process_response` into the session and surface on the next request — verified end-to-end with `Client(HTTP_HOST='127.0.0.1')` against `/accounts/<pk>/delete/`.
- For the same reason, the `delete()` hook on `DeletionMixin` is misleading documentation — do not rely on it in any view that extends `BaseDeleteView` / `DeleteView` / `SingleObjectTemplateResponseMixin`.

Related: [[post-save-connection-inspection]] — another case where Django's runtime behaviour diverged from a previously-known API.
