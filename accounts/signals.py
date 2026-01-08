from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import Profile
from staff.models import staff

User = get_user_model()

@receiver(post_save, sender=User)
def create_related_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.role == "staff":
            staff.objects.get_or_create(user=instance)