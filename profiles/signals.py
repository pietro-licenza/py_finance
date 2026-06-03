from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a Profile automatically whenever a new User is created."""
    if created:
        Profile.objects.create(user=instance)
