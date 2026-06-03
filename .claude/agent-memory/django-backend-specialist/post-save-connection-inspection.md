---
name: post-save-connection-inspection
description: How to inspect Django post_save receivers for a given sender in Django 6.0 (the _live_receivers API returns weird nested structures)
metadata:
  type: reference
---

To verify a `@receiver(post_save, sender=User)` is actually wired up at runtime, walk `post_save.receivers` directly — NOT `post_save._live_receivers(sender=...)`, which returns nested structures that vary by Django version and are hard to parse.

**Why:** On Django 6.0, `post_save._live_receivers(User)` returned `[(<function create_profile>,), []]` (a mixed list of tuples and empty lists) — printing each entry as `entry.__module__` raised `AttributeError: 'list' object has no attribute '__module__'`. Iterating `post_save.receivers` directly returns the canonical 4-tuple `(lookup_key, receiver_weakref, sender_weakref, is_disconnected)` for every connection, which is stable.

**How to apply:** When debugging whether a signal handler is connected (especially after a Sprint 1-style "wire up signals in `ready()`" task), use this snippet instead of `_live_receivers`:

```python
from django.db.models.signals import post_save
for receiver in post_save.receivers:
    _, recv_ref, sender_ref, _ = receiver
    print(recv_ref(), 'listens to', sender_ref())
```

The reference at index 0 (`lookup_key`) and the boolean at index 3 (`is_disconnected`) are for the dispatcher's internal use — ignore them when you're just checking "is handler X connected to sender Y?"
