from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Per-user profile that stores additional information beyond the User model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    full_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'
        ordering = ['user__email']

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.user.email
