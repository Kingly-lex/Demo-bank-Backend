from django.dispatch import receiver
from .models import Profile
from apps.users.models import User
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)
